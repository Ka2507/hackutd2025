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
    
    async def _call_llm(self, prompt: str, model: str = "local") -> str:
        """
        Call LLM (local Ollama or Nemotron)
        
        Args:
            prompt: The prompt to send
            model: "local" for Ollama or "nemotron" for NVIDIA API
            
        Returns:
            LLM response text
        """
        # This is a placeholder - will be implemented with actual LLM calls
        # For MVP, we'll simulate responses
        logger.info(f"Agent {self.name} calling {model} LLM")
        
        # Simulate different agent responses
        if "market" in prompt.lower() or "strategy" in prompt.lower():
            return "Market analysis complete. Target segment identified: B2B SaaS companies."
        elif "research" in prompt.lower() or "competitor" in prompt.lower():
            return "Research synthesis: 3 key competitors identified with gaps in AI automation."
        elif "user stor" in prompt.lower() or "backlog" in prompt.lower():
            return "Generated 5 user stories with acceptance criteria and story points."
        elif "prototype" in prompt.lower() or "design" in prompt.lower():
            return "Prototype mockups created with modern UI/UX patterns."
        elif "launch" in prompt.lower() or "gtm" in prompt.lower():
            return "Go-to-market strategy: Multi-channel approach with focus on product-led growth."
        elif "automat" in prompt.lower():
            return "Automation workflows configured for sprint summaries and standup reports."
        elif "regulation" in prompt.lower() or "compliance" in prompt.lower():
            return "Compliance check complete. GDPR and SOC2 requirements identified."
        else:
            return f"Agent {self.name} processing task with {model} model."
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', status='{self.status}')>"

