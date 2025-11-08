"""
Nemotron Bridge - Handles NVIDIA Nemotron API calls for high-level reasoning
Minimizes API calls to stay within budget ($40 cap)
"""
import aiohttp
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger
from .cost_aware_orchestrator import CostAwareOrchestrator


class NemotronBridge:
    """
    Bridge to NVIDIA Nemotron for strategic reasoning
    Caches responses and limits calls to stay under budget
    """
    
    def __init__(self):
        self.api_key = settings.nemotron_api_key
        self.base_url = settings.nemotron_base_url
        self.model = settings.nemotron_model
        self.max_calls = settings.nemotron_max_calls
        self.call_count = 0
        self.call_history = []
        self.response_cache = {}
        self.cost_orchestrator = CostAwareOrchestrator(total_budget=40.0)
        
        if not self.api_key:
            logger.warning("NEMOTRON_API_KEY not set. Nemotron features will be simulated.")
    
    def _should_use_nemotron(self, task_type: str, priority: str = "medium") -> bool:
        """
        Determine if we should use Nemotron for this task
        Only use for high-value, strategic tasks
        
        Args:
            task_type: Type of task
            priority: Task priority
            
        Returns:
            True if Nemotron should be used
        """
        if self.call_count >= self.max_calls:
            logger.warning(f"Nemotron call limit reached ({self.max_calls})")
            return False
        
        # Only use Nemotron for strategic, high-priority tasks
        high_value_tasks = [
            "orchestration",
            "strategic_planning",
            "complex_reasoning",
            "multi_agent_coordination"
        ]
        
        return task_type in high_value_tasks and priority == "high"
    
    async def call_nemotron(
        self, 
        prompt: str, 
        task_type: str = "general",
        priority: str = "medium",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Call Nemotron API for reasoning
        
        Args:
            prompt: The prompt to send
            task_type: Type of task
            priority: Task priority
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response from Nemotron
        """
        # Use cost-aware orchestrator to decide
        should_use, value_score = self.cost_orchestrator.should_use_nemotron(
            task_type=task_type,
            task_description=prompt[:200],
            context={"priority": priority}
        )
        
        if not should_use:
            logger.info(f"Using local LLM instead of Nemotron for {task_type} (value score: {value_score:.2f})")
            return await self._fallback_to_local(prompt)
        
        # Check legacy method as backup
        if not self._should_use_nemotron(task_type, priority):
            logger.info(f"Using local LLM instead of Nemotron for {task_type}")
            return await self._fallback_to_local(prompt)
        
        # Check cache
        cache_key = f"{prompt[:100]}_{task_type}"
        if cache_key in self.response_cache:
            logger.info("Returning cached Nemotron response")
            return self.response_cache[cache_key]
        
        # Make API call
        if not self.api_key:
            logger.warning("Nemotron API key not configured, using fallback")
            return await self._fallback_to_local(prompt)
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Nemotron, a strategic AI reasoning engine helping coordinate multiple AI agents for product management tasks."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "success": True,
                            "response": data["choices"][0]["message"]["content"],
                            "model": self.model,
                            "usage": data.get("usage", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Update call count and history
                        self.call_count += 1
                        self.call_history.append({
                            "task_type": task_type,
                            "timestamp": result["timestamp"],
                            "tokens": result["usage"].get("total_tokens", 0)
                        })
                        
                        # Track cost
                        self.cost_orchestrator._track_cost(result)
                        
                        # Cache response
                        self.response_cache[cache_key] = result
                        
                        logger.info(f"Nemotron call successful ({self.call_count}/{self.max_calls})")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Nemotron API error: {response.status} - {error_text}")
                        return await self._fallback_to_local(prompt)
                        
        except Exception as e:
            logger.error(f"Error calling Nemotron: {str(e)}")
            return await self._fallback_to_local(prompt)
    
    async def _fallback_to_local(self, prompt: str) -> Dict[str, Any]:
        """
        Fallback to local LLM reasoning
        
        Args:
            prompt: The prompt
            
        Returns:
            Simulated response
        """
        # Simulate local LLM processing
        logger.info("Using local LLM fallback")
        
        # Generate contextual response based on prompt keywords
        response = self._generate_fallback_response(prompt)
        
        return {
            "success": True,
            "response": response,
            "model": "local_fallback",
            "usage": {"total_tokens": len(response.split())},
            "timestamp": datetime.now().isoformat(),
            "note": "Generated by local LLM, not Nemotron"
        }
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate contextual fallback response"""
        prompt_lower = prompt.lower()
        
        if "orchestrat" in prompt_lower or "coordinat" in prompt_lower:
            return """Multi-agent orchestration plan:
            1. Strategy Agent analyzes market and defines objectives
            2. Research Agent gathers data and validates assumptions
            3. Dev Agent translates requirements into actionable stories
            4. Prototype Agent creates visual representations
            5. GTM Agent develops go-to-market strategy
            6. Automation Agent streamlines workflows
            7. Regulation Agent ensures compliance
            
            This sequential flow with shared context ensures coherent outputs."""
        
        elif "strategic" in prompt_lower or "planning" in prompt_lower:
            return """Strategic approach:
            - Focus on high-impact, high-feasibility initiatives
            - Balance short-term wins with long-term vision
            - Leverage AI capabilities for competitive advantage
            - Prioritize user needs and pain points
            - Maintain flexibility for market changes"""
        
        elif "reasoning" in prompt_lower or "decision" in prompt_lower:
            return """Decision framework:
            1. Define success criteria
            2. Gather relevant data
            3. Generate alternatives
            4. Evaluate trade-offs
            5. Make recommendation with confidence level
            6. Plan for monitoring and iteration"""
        
        else:
            return """Based on analysis of the task requirements and available context,
            the recommended approach is to leverage multiple agents in coordination,
            with each contributing their specialized capabilities. Priority should be
            given to strategic alignment and user value delivery."""
    
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
        prompt = f"""
        Task: {task}
        
        Available Agents: {', '.join(available_agents)}
        
        Context: {context}
        
        Create a detailed orchestration plan that:
        1. Determines which agents to use
        2. Defines the sequence of agent execution
        3. Specifies what information flows between agents
        4. Identifies potential conflicts and how to resolve them
        5. Estimates overall execution time and confidence
        
        Provide the plan in a structured format.
        """
        
        response = await self.call_nemotron(
            prompt,
            task_type="orchestration",
            priority="high",
            max_tokens=1500
        )
        
        # Parse response into structured plan
        plan = {
            "task": task,
            "orchestration_response": response["response"],
            "agents_to_use": self._extract_agents(response["response"], available_agents),
            "estimated_duration": "5-10 minutes",
            "confidence": 0.85,
            "model_used": response["model"]
        }
        
        return plan
    
    def _extract_agents(self, text: str, available_agents: List[str]) -> List[str]:
        """Extract mentioned agents from text"""
        mentioned = []
        text_lower = text.lower()
        for agent in available_agents:
            if agent.lower() in text_lower:
                mentioned.append(agent)
        return mentioned if mentioned else available_agents[:3]
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        total_tokens = sum(call.get("tokens", 0) for call in self.call_history)
        budget_status = self.cost_orchestrator.get_budget_status()
        
        return {
            "calls_made": self.call_count,
            "calls_remaining": max(0, self.max_calls - self.call_count),
            "max_calls": self.max_calls,
            "total_tokens": total_tokens,
            "cached_responses": len(self.response_cache),
            "call_history": self.call_history[-10:],  # Last 10 calls
            "budget": budget_status
        }
    
    def reset_limits(self):
        """Reset call limits (e.g., for new billing period)"""
        self.call_count = 0
        self.call_history = []
        logger.info("Nemotron call limits reset")


# Global instance
nemotron_bridge = NemotronBridge()

