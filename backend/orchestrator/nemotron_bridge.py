"""
Nemotron Bridge - Real NVIDIA Nemotron API integration
Uses different models for different agents to optimize cost and performance
"""
from openai import OpenAI
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger


# Model mapping based on agent needs
AGENT_MODEL_MAP = {
    # High-complexity strategic reasoning - use Super model
    "strategy": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "risk_assessment": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    
    # Compliance and regulatory - use reasoning model
    "regulation": "nvidia/llama-3.1-nemotron-70b-instruct",
    
    # Standard agents - use efficient Nano model
    "research": "nvidia/llama-3.1-nemotron-70b-instruct",
    "dev": "nvidia/llama-3.1-nemotron-70b-instruct",
    "prototype": "nvidia/llama-3.1-nemotron-70b-instruct",
    "gtm": "nvidia/llama-3.1-nemotron-70b-instruct",
    "automation": "nvidia/llama-3.1-nemotron-70b-instruct",
    "prioritization": "nvidia/llama-3.1-nemotron-70b-instruct",
    "prd": "nvidia/llama-3.1-nemotron-70b-instruct",
    
    # Default
    "default": "nvidia/llama-3.1-nemotron-70b-instruct"
}

# Estimated costs per 1M tokens (approximate)
MODEL_COSTS = {
    "nvidia/llama-3.3-nemotron-super-49b-v1.5": 0.003,  # $3 per 1M tokens
    "nvidia/llama-3.1-nemotron-70b-instruct": 0.001,   # $1 per 1M tokens
}


class NemotronBridge:
    """
    Bridge to NVIDIA Nemotron API for real AI reasoning
    Optimizes model selection and tracks costs against $60 budget
    """
    
    def __init__(self):
        self.api_key = settings.nemotron_api_key
        self.base_url = settings.nemotron_base_url
        self.total_budget = settings.total_budget
        self.budget_warning_threshold = settings.budget_warning_threshold
        
        self.call_count = 0
        self.call_history = []
        self.response_cache = {}
        self.total_cost = 0.0
        
        # Initialize OpenAI client for NVIDIA
        if self.api_key:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            logger.info("✅ NVIDIA Nemotron API client initialized")
        else:
            self.client = None
            logger.warning("⚠️ NEMOTRON_API_KEY not set. API features will be simulated.")
    
    def get_model_for_agent(self, agent_name: str) -> str:
        """Get the appropriate model for an agent"""
        return AGENT_MODEL_MAP.get(agent_name, AGENT_MODEL_MAP["default"])
    
    def estimate_cost(self, tokens: int, model: str) -> float:
        """Estimate cost for a number of tokens"""
        cost_per_1m = MODEL_COSTS.get(model, 0.001)
        return (tokens / 1_000_000) * cost_per_1m
    
    def can_afford_call(self, estimated_tokens: int = 2000, model: str = None) -> bool:
        """Check if we can afford this call within budget"""
        if model is None:
            model = AGENT_MODEL_MAP["default"]
        
        estimated_cost = self.estimate_cost(estimated_tokens, model)
        remaining_budget = self.total_budget - self.total_cost
        
        if estimated_cost > remaining_budget:
            logger.warning(f"❌ Budget exceeded! Estimated: ${estimated_cost:.4f}, Remaining: ${remaining_budget:.4f}")
            return False
        
        if remaining_budget < (self.total_budget * 0.1):  # Less than 10% remaining
            logger.warning(f"⚠️ Budget low! Only ${remaining_budget:.2f} remaining")
        
        return True
    
    async def call_nemotron(
        self, 
        prompt: str, 
        agent_name: str = "default",
        task_type: str = "general",
        priority: str = "medium",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call NVIDIA Nemotron API with appropriate model for the agent
        
        Args:
            prompt: The user prompt
            agent_name: Name of the calling agent (determines model)
            task_type: Type of task
            priority: Task priority
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            system_prompt: Optional custom system prompt
            
        Returns:
            Response with content, model used, usage stats, and cost
        """
        # Check cache first
        cache_key = f"{agent_name}:{prompt[:100]}:{task_type}"
        if cache_key in self.response_cache:
            logger.info(f"💾 Returning cached response for {agent_name}")
            cached = self.response_cache[cache_key]
            cached["cached"] = True
            return cached
        
        # Check if API key is available
        if not self.client:
            logger.warning(f"⚠️ No API key - using simulated response for {agent_name}")
            return await self._fallback_to_simulated(prompt, agent_name)
        
        # Select model for this agent
        model = self.get_model_for_agent(agent_name)
        
        # Check budget
        if not self.can_afford_call(max_tokens, model):
            logger.warning(f"💰 Budget limit reached - using simulated response for {agent_name}")
            return await self._fallback_to_simulated(prompt, agent_name)
        
        try:
            logger.info(f"🚀 Calling NVIDIA API | Agent: {agent_name} | Model: {model}")
            
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system",
                    "content": f"You are an expert AI agent specialized in {agent_name} for product management. Provide detailed, actionable insights."
                })
            
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95
            )
            
            # Extract response
            response_text = completion.choices[0].message.content
            usage = completion.usage
            
            # Calculate cost
            total_tokens = usage.total_tokens
            cost = self.estimate_cost(total_tokens, model)
            self.total_cost += cost
            
            # Track call
            self.call_count += 1
            call_record = {
                "agent": agent_name,
                "model": model,
                "task_type": task_type,
                "timestamp": datetime.now().isoformat(),
                "tokens": {
                    "prompt": usage.prompt_tokens,
                    "completion": usage.completion_tokens,
                    "total": total_tokens
                },
                "cost": cost,
                "cumulative_cost": self.total_cost
            }
            self.call_history.append(call_record)
            
            result = {
                "success": True,
                "response": response_text,
                "model": model,
                "agent": agent_name,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": total_tokens
                },
                "cost": cost,
                "cumulative_cost": self.total_cost,
                "timestamp": datetime.now().isoformat(),
                "cached": False
            }
            
            # Cache the response
            self.response_cache[cache_key] = result
            
            logger.info(f"✅ NVIDIA call successful | Tokens: {total_tokens} | Cost: ${cost:.4f} | Total: ${self.total_cost:.2f}/${self.total_budget}")
            
            # Check if approaching budget
            if self.total_cost >= self.budget_warning_threshold:
                logger.warning(f"⚠️ BUDGET WARNING: ${self.total_cost:.2f}/${self.total_budget} used!")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error calling NVIDIA API for {agent_name}: {str(e)}")
            logger.info(f"↩️ Falling back to simulated response")
            return await self._fallback_to_simulated(prompt, agent_name)
    
    async def _fallback_to_simulated(self, prompt: str, agent_name: str) -> Dict[str, Any]:
        """
        Fallback to simulated response when API is unavailable or budget exceeded
        """
        logger.info(f"🔄 Using simulated response for {agent_name}")
        
        # Generate contextual response based on agent and prompt
        response = self._generate_simulated_response(prompt, agent_name)
        
        return {
            "success": True,
            "response": response,
            "model": "simulated_fallback",
            "agent": agent_name,
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            },
            "cost": 0.0,
            "cumulative_cost": self.total_cost,
            "timestamp": datetime.now().isoformat(),
            "note": "⚠️ Simulated response (no API call made)",
            "cached": False
        }
    
    def _generate_simulated_response(self, prompt: str, agent_name: str) -> str:
        """Generate a contextual simulated response"""
        prompt_lower = prompt.lower()
        
        # Agent-specific responses
        if agent_name == "strategy":
            return f"""Strategic Analysis:

Market Opportunity: Based on the prompt, this represents a significant market opportunity with growing demand.

Key Success Factors:
1. Strong product-market fit
2. Competitive differentiation
3. Scalable execution plan
4. Customer-centric approach

Recommendation: Proceed with phased approach, starting with MVP to validate assumptions."""
        
        elif agent_name == "research":
            return f"""Research Insights:

User Needs Analysis:
- Primary pain points identified through user feedback
- Market trends showing 40% year-over-year growth
- Competitive landscape analysis reveals opportunities

Key Findings:
1. Strong user demand for this solution
2. Existing solutions have gaps we can fill
3. Target market is underserved

Recommendation: Focus on addressing top 3 user pain points first."""
        
        elif agent_name == "dev":
            return f"""Development Plan:

User Stories Generated: 15 stories

Priority 1 (Must Have):
- User authentication and security
- Core feature functionality
- Basic analytics dashboard

Priority 2 (Should Have):
- Advanced integrations
- Customization options
- Reporting features

Technical Stack Recommendations:
- Proven, scalable technologies
- Modern best practices
- Security-first approach"""
        
        else:
            return f"""{agent_name.title()} Analysis:

Based on the requirements provided, here are the key recommendations:

1. Focus on delivering maximum value to users
2. Ensure technical feasibility and scalability
3. Maintain alignment with business objectives
4. Plan for iterative improvement

Next Steps:
- Validate assumptions with stakeholders
- Create detailed specifications
- Begin phased implementation"""
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get detailed usage statistics and budget status"""
        total_tokens = sum(
            call["tokens"]["total"] 
            for call in self.call_history 
            if "tokens" in call
        )
        
        # Calculate budget status
        budget_remaining = self.total_budget - self.total_cost
        percentage_used = (self.total_cost / self.total_budget) * 100
        
        # Get model breakdown
        model_usage = {}
        for call in self.call_history:
            model = call.get("model", "unknown")
            if model not in model_usage:
                model_usage[model] = {"calls": 0, "tokens": 0, "cost": 0.0}
            model_usage[model]["calls"] += 1
            model_usage[model]["tokens"] += call.get("tokens", {}).get("total", 0)
            model_usage[model]["cost"] += call.get("cost", 0.0)
        
        return {
            "calls_made": self.call_count,
            "total_tokens": total_tokens,
            "cached_responses": len(self.response_cache),
            "call_history": self.call_history[-10:],  # Last 10 calls
            "budget": {
                "total_budget": self.total_budget,
                "used_budget": round(self.total_cost, 4),
                "remaining_budget": round(budget_remaining, 4),
                "percentage_used": round(percentage_used, 2),
                "budget_status": self._get_budget_status(percentage_used),
                "warning": percentage_used >= 85
            },
            "model_usage": model_usage
        }
    
    def _get_budget_status(self, percentage: float) -> str:
        """Get budget status level"""
        if percentage >= 95:
            return "critical"
        elif percentage >= 85:
            return "warning"
        elif percentage >= 70:
            return "moderate"
        else:
            return "healthy"
    
    async def orchestrate_agents(
        self,
        task: str,
        available_agents: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use Nemotron to orchestrate multiple agents for a complex task
        
        Args:
            task: The high-level task
            available_agents: List of available agent names
            context: Current context and constraints
            
        Returns:
            Orchestration plan
        """
        prompt = f"""You are orchestrating multiple AI agents for a product management task.

Task: {task}

Available Agents: {', '.join(available_agents)}

Context: {context}

Create a plan that:
1. Determines which agents to use and in what order
2. Specifies what information each agent needs
3. Identifies how agents should collaborate
4. Estimates confidence and timeline

Provide a clear, actionable orchestration plan."""
        
        result = await self.call_nemotron(
            prompt=prompt,
            agent_name="orchestration",
            task_type="orchestration",
            temperature=0.7,
            max_tokens=1500
        )
        
        return {
            "task": task,
            "orchestration_response": result["response"],
            "agents_to_use": available_agents,
            "estimated_duration": "5-10 minutes",
            "confidence": 0.85,
            "model_used": result["model"]
        }
    
    def reset_limits(self):
        """Reset call limits and budget tracking"""
        self.call_count = 0
        self.call_history = []
        self.total_cost = 0.0
        self.response_cache = {}
        logger.info("🔄 Nemotron limits and budget reset")


# Global instance
nemotron_bridge = NemotronBridge()
