"""
Agent Collaboration System - Enables agents to validate and refine each other's work
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from orchestrator.nemotron_bridge import nemotron_bridge
from utils.logger import logger


class AgentCollaboration:
    """Manages collaboration between agents"""
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.collaboration_history = []
    
    async def validate_with_peer(
        self,
        agent_name: str,
        output: Dict[str, Any],
        validator_agent_name: str,
        validation_criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Have one agent validate another agent's output
        
        Args:
            agent_name: Name of agent that produced output
            output: Output to validate
            validator_agent_name: Name of agent doing validation
            validation_criteria: Specific criteria to check
            
        Returns:
            Validation result with score and feedback
        """
        logger.info(f"{validator_agent_name} validating {agent_name} output")
        
        validator_agent = self.agents.get(validator_agent_name)
        if not validator_agent:
            return {
                "validated": False,
                "error": f"Validator agent {validator_agent_name} not found"
            }
        
        # Build validation prompt
        validation_prompt = self._build_validation_prompt(
            agent_name,
            output,
            validation_criteria
        )
        
        # Use validator agent to validate
        validation_result = await validator_agent.execute({
            "task_type": "validation",
            "output_to_validate": output,
            "validation_criteria": validation_criteria or [
                "accuracy",
                "completeness",
                "consistency",
                "relevance"
            ]
        })
        
        # Extract validation score
        validation_score = self._extract_validation_score(validation_result)
        
        result = {
            "validated": True,
            "validator": validator_agent_name,
            "validated_agent": agent_name,
            "validation_score": validation_score,
            "confidence": validation_score,
            "feedback": validation_result.get("result", {}).get("feedback", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        self.collaboration_history.append(result)
        return result
    
    async def request_refinement(
        self,
        agent_name: str,
        original_output: Dict[str, Any],
        feedback: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Request an agent to refine its output based on feedback
        
        Args:
            agent_name: Name of agent to refine
            original_output: Original output
            feedback: Feedback for improvement
            context: Additional context
            
        Returns:
            Refined output
        """
        logger.info(f"Requesting refinement from {agent_name}")
        
        agent = self.agents.get(agent_name)
        if not agent:
            return {
                "refined": False,
                "error": f"Agent {agent_name} not found"
            }
        
        # Build refinement prompt
        refinement_result = await agent.execute({
            "task_type": "refinement",
            "original_output": original_output,
            "feedback": feedback,
            "context": context
        })
        
        result = {
            "refined": True,
            "agent": agent_name,
            "original_output": original_output,
            "refined_output": refinement_result.get("result", {}),
            "feedback_applied": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        self.collaboration_history.append(result)
        return result
    
    async def cross_validate(
        self,
        outputs: List[Dict[str, Any]],
        validator_agent_name: str
    ) -> Dict[str, Any]:
        """
        Cross-validate multiple agent outputs for consistency
        
        Args:
            outputs: List of outputs from different agents
            validator_agent_name: Agent to perform validation
            
        Returns:
            Cross-validation result
        """
        logger.info(f"Cross-validating {len(outputs)} outputs with {validator_agent_name}")
        
        validator_agent = self.agents.get(validator_agent_name)
        if not validator_agent:
            return {
                "validated": False,
                "error": f"Validator agent {validator_agent_name} not found"
            }
        
        # Use Nemotron for complex cross-validation
        prompt = f"""
        Cross-validate these outputs from different agents for consistency:
        
        {[{'agent': o.get('agent', ''), 'output': o.get('result', {})} for o in outputs]}
        
        Check for:
        1. Contradictions between outputs
        2. Missing information that should be present
        3. Inconsistencies in assumptions
        4. Alignment with overall goal
        
        Provide validation score and specific feedback.
        """
        
        validation_response = await nemotron_bridge.call_nemotron(
            prompt=prompt,
            task_type="validation",
            priority="medium",
            max_tokens=800
        )
        
        return {
            "validated": True,
            "validator": validator_agent_name,
            "outputs_count": len(outputs),
            "validation_score": 0.8,  # Extract from response
            "feedback": validation_response["response"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_validation_prompt(
        self,
        agent_name: str,
        output: Dict[str, Any],
        criteria: Optional[List[str]]
    ) -> str:
        """Build validation prompt"""
        criteria_text = ", ".join(criteria) if criteria else "accuracy, completeness, consistency"
        
        return f"""
        Validate this output from {agent_name}:
        
        Output: {output}
        
        Check for:
        {criteria_text}
        
        Provide:
        1. Validation score (0-1)
        2. Specific feedback
        3. Suggestions for improvement
        """
    
    def _extract_validation_score(self, validation_result: Dict[str, Any]) -> float:
        """Extract validation score from result"""
        result_data = validation_result.get("result", {})
        
        # Look for score in result
        if "score" in result_data:
            return float(result_data["score"])
        
        if "validation_score" in result_data:
            return float(result_data["validation_score"])
        
        # Default based on status
        if validation_result.get("status") == "completed":
            return 0.8
        else:
            return 0.5
    
    def get_collaboration_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent collaboration history"""
        return self.collaboration_history[-limit:]



