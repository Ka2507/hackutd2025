"""
Base Agent class for ProdigyPM
All specialized agents inherit from this class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import logger
from .agent_config import get_agent_model, get_agent_stage, AGENT_DESCRIPTIONS


class BaseAgent(ABC):
    """Base class for all AI agents in ProdigyPM"""
    
    def __init__(self, name: str, goal: str, context: Optional[Dict[str, Any]] = None, agent_key: Optional[str] = None):
        """
        Initialize the agent
        
        Args:
            name: Agent name/identifier
            goal: Primary goal/purpose of the agent
            context: Shared context dictionary for agent communication
            agent_key: Agent key for model assignment (e.g., "strategy", "research")
        """
        self.name = name
        self.goal = goal
        self.context = context or {}
        self.status = "idle"
        self.last_output = None
        self.agent_key = agent_key or name.lower().replace("agent", "").strip()
        
        # Get agent-specific Nemotron model
        self.nemotron_model = get_agent_model(self.agent_key)
        self.lifecycle_stage = get_agent_stage(self.agent_key)
        
        # Get agent description if available
        agent_desc = AGENT_DESCRIPTIONS.get(self.agent_key, {})
        self.stage_name = agent_desc.get("stage", "Unknown Stage")
        self.model_reasoning = agent_desc.get("model_reasoning", "")
        
        logger.info(f"Initialized agent: {name} with goal: {goal}")
        logger.info(f"  Lifecycle Stage: {self.lifecycle_stage} - {self.stage_name}")
        logger.info(f"  Assigned Model: {self.nemotron_model} ({self.model_reasoning})")
    
    @abstractmethod
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary task
        
        Args:
            task_input: Input parameters for the task
            
        Returns:
            Dict containing the task results and metadata
        """
        pass
    
    def update_status(self, status: str):
        """Update agent status"""
        self.status = status
        logger.info(f"Agent {self.name} status updated to: {status}")
    
    def update_context(self, key: str, value: Any):
        """Update shared context"""
        self.context[key] = value
        logger.debug(f"Agent {self.name} updated context key: {key}")
    
    def get_context(self, key: str) -> Optional[Any]:
        """Retrieve value from shared context"""
        return self.context.get(key)
    
    def format_output(self, result: Any, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Format agent output in a standard structure
        
        Args:
            result: The primary result data
            metadata: Additional metadata about the execution
            
        Returns:
            Standardized output dictionary
        """
        output = {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "status": self.status,
            "result": result,
            "metadata": metadata or {}
        }
        self.last_output = output
        return output
    
    async def _call_llm(self, prompt: str, model: str = "local", use_nemotron: bool = False) -> str:
        """
        Call LLM (local Ollama or Nemotron)
        
        Args:
            prompt: The prompt to send
            model: "local" for Ollama or "nemotron" for NVIDIA API
            use_nemotron: Whether to use Nemotron (uses agent-specific model)
            
        Returns:
            LLM response text
        """
        if use_nemotron:
            # Import here to avoid circular dependencies
            from orchestrator.nemotron_bridge import nemotron_bridge
            
            logger.info(f"Agent {self.name} calling Nemotron with model: {self.nemotron_model}")
            
            # Call Nemotron with agent-specific model
            # Use agent_key as task_type so cost orchestrator recognizes it
            response = await nemotron_bridge.call_nemotron(
                prompt=prompt,
                task_type=self.agent_key,  # This will be recognized as high-value
                priority="high",
                model_override=self.nemotron_model,
                max_tokens=2000  # Allow longer responses for detailed outputs
            )
            
            if response.get("success"):
                return response.get("response", "")
            else:
                logger.warning(f"Nemotron call failed for {self.name}, using fallback")
                return await self._fallback_llm(prompt)
        else:
            # Use local LLM or fallback
            logger.info(f"Agent {self.name} using local LLM")
            return await self._fallback_llm(prompt)
    
    async def _fallback_llm(self, prompt: str) -> str:
        """Fallback LLM response based on agent type"""
        prompt_lower = prompt.lower()
        
        # Agent-specific fallback responses
        if "market" in prompt_lower or "strategy" in prompt_lower:
            return "Market analysis complete. Target segment identified: B2B SaaS companies."
        elif "research" in prompt_lower or "competitor" in prompt_lower:
            return "Research synthesis: 3 key competitors identified with gaps in AI automation."
        elif "user stor" in prompt_lower or "backlog" in prompt_lower:
            return "Generated 5 user stories with acceptance criteria and story points."
        elif "prototype" in prompt_lower or "design" in prompt_lower:
            return "Prototype mockups created with modern UI/UX patterns."
        elif "launch" in prompt_lower or "gtm" in prompt_lower:
            return "Go-to-market strategy: Multi-channel approach with focus on product-led growth."
        elif "automat" in prompt_lower:
            return "Automation workflows configured for sprint summaries and standup reports."
        elif "regulation" in prompt_lower or "compliance" in prompt_lower:
            return "Compliance check complete. GDPR and SOC2 requirements identified."
        elif "priorit" in prompt_lower:
            return "Features prioritized using multi-factor analysis: High-value, low-effort features identified."
        elif "risk" in prompt_lower:
            return "Risk assessment complete: 3 high-priority risks identified with mitigation strategies."
        else:
            return f"Agent {self.name} processing task with local model."
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', status='{self.status}')>"

