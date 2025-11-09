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
from orchestrator.nemotron_bridge import nemotron_bridge


class BaseAgent(ABC):
    """Base class for all AI agents in ProdigyPM"""
    
    def __init__(self, name: str, goal: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent
        
        Args:
            name: Agent name/identifier
            goal: Primary goal/purpose of the agent
            context: Shared context dictionary for agent communication
        """
        self.name = name
        self.goal = goal
        self.context = context or {}
        self.status = "idle"
        self.last_output = None
        logger.info(f"Initialized agent: {name} with goal: {goal}")
    
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
    
    async def _call_llm(self, prompt: str, use_nvidia: bool = True, use_cache: bool = False) -> str:
        """
        Call LLM - Uses real NVIDIA Nemotron API
        
        Args:
            prompt: The prompt to send
            use_nvidia: Whether to use NVIDIA API (default True)
            use_cache: Whether to cache responses (default False for interactive chat)
            
        Returns:
            LLM response text
        """
        if use_nvidia:
            # Use real NVIDIA API through nemotron_bridge
            agent_key = self.name.lower().replace("agent", "").strip()
            
            result = await nemotron_bridge.call_nemotron(
                prompt=prompt,
                agent_name=agent_key,
                task_type=self._get_task_type(prompt),
                temperature=0.7,
                max_tokens=1500,
                use_cache=use_cache  # Disable caching for interactive chat
            )
            
            return result["response"]
        else:
            # Fallback for testing without API
            return f"Agent {self.name} processed: {prompt[:50]}..."
    
    def _get_task_type(self, prompt: str) -> str:
        """Determine task type from prompt for budget optimization"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["market", "strategy", "competitive"]):
            return "strategic_planning"
        elif any(word in prompt_lower for word in ["research", "user", "trend"]):
            return "research"
        elif any(word in prompt_lower for word in ["compliance", "regulation", "risk"]):
            return "compliance"
        elif any(word in prompt_lower for word in ["priorit", "rank", "score"]):
            return "prioritization"
        else:
            return "general"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', status='{self.status}')>"

