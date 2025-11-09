"""
Task Graph - LangGraph-based orchestration for multi-agent workflows
Coordinates agent execution with shared context
"""
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import asyncio
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from agents import (
    StrategyAgent, ResearchAgent, DevAgent, PrototypeAgent,
    GtmAgent, AutomationAgent, RegulationAgent,
    PrioritizationAgent, RiskAssessmentAgent, PRDAgent
)
from .memory_manager import memory_manager
from .nemotron_bridge import nemotron_bridge
from utils.logger import logger


class WorkflowType(Enum):
    """Predefined workflow types"""
    FULL_FEATURE_PLANNING = "full_feature_planning"
    RESEARCH_AND_STRATEGY = "research_and_strategy"
    DEV_PLANNING = "dev_planning"
    LAUNCH_PLANNING = "launch_planning"
    COMPLIANCE_CHECK = "compliance_check"
    CUSTOM = "custom"


class TaskGraph:
    """
    Orchestrates multi-agent workflows using a graph-based approach
    Similar to LangGraph but simplified for MVP
    """
    
    def __init__(self):
        """Initialize task graph with all agents"""
        self.shared_context = {}
        self.agents = {
            "strategy": StrategyAgent(self.shared_context),
            "research": ResearchAgent(self.shared_context),
            "dev": DevAgent(self.shared_context),
            "prototype": PrototypeAgent(self.shared_context),
            "gtm": GtmAgent(self.shared_context),
            "automation": AutomationAgent(self.shared_context),
            "regulation": RegulationAgent(self.shared_context),
            "prioritization": PrioritizationAgent(self.shared_context),
            "risk_assessment": RiskAssessmentAgent(self.shared_context),
            "prd": PRDAgent(self.shared_context)
        }
        self.workflow_history = []
        logger.info("TaskGraph initialized with all agents")
    
    async def execute_workflow(
        self,
        workflow_type: str,
        input_data: Dict[str, Any],
        project_id: Optional[int] = None,
        use_nemotron: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a predefined workflow
        
        Args:
            workflow_type: Type of workflow to execute
            input_data: Input parameters for the workflow
            project_id: Project ID for context storage
            use_nemotron: Whether to use Nemotron for orchestration
            
        Returns:
            Workflow results
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Starting workflow {workflow_id}: {workflow_type}")
        
        # Get orchestration plan from Nemotron if enabled
        if use_nemotron:
            orchestration_plan = await nemotron_bridge.orchestrate_agents(
                task=f"{workflow_type} workflow",
                available_agents=list(self.agents.keys()),
                context=input_data
            )
            logger.info(f"Nemotron orchestration: {orchestration_plan}")
        
        # Execute appropriate workflow
        workflow_map = {
            WorkflowType.FULL_FEATURE_PLANNING.value: self._full_feature_planning,
            WorkflowType.RESEARCH_AND_STRATEGY.value: self._research_and_strategy,
            WorkflowType.DEV_PLANNING.value: self._dev_planning,
            WorkflowType.LAUNCH_PLANNING.value: self._launch_planning,
            WorkflowType.COMPLIANCE_CHECK.value: self._compliance_check,
        }
        
        workflow_func = workflow_map.get(workflow_type, self._custom_workflow)
        
        try:
            result = await workflow_func(input_data, project_id)
            
            # Store workflow in memory
            self._store_workflow_memory(workflow_id, workflow_type, input_data, result, project_id)
            
            result["workflow_id"] = workflow_id
            result["status"] = "completed"
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e)
            }
    
    async def _full_feature_planning(
        self, 
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """
        Full feature planning workflow with PRD generation.
        
        Lifecycle: Strategy → Research → Prioritization → Dev → 
        Prototype → GTM → Automation → Regulation → Risk → PRD
        """
        results = {"workflow": "full_feature_planning", "steps": []}
        
        # Step 1: Strategy Agent
        logger.info("Step 1: Strategy Agent")
        strategy_result = await self.agents["strategy"].execute({
            "task_type": "idea_generation",
            "product_idea": input_data.get("feature", ""),
            "target_market": input_data.get("market", "")
        })
        results["steps"].append(strategy_result)
        
        # Step 2: Research Agent
        logger.info("Step 2: Research Agent")
        research_result = await self.agents["research"].execute({
            "task_type": "user_research",
            "query": input_data.get("feature", ""),
            "sources": ["reddit", "twitter", "product_hunt"]
        })
        results["steps"].append(research_result)
        
        # Step 3: Prioritization Agent
        logger.info("Step 3: Prioritization Agent")
        prioritization_result = await self.agents["prioritization"].execute({
            "task_type": "prioritize",
            "features": input_data.get("features", []),
            "context": {"strategy": strategy_result, "research": research_result}
        })
        results["steps"].append(prioritization_result)
        
        # Step 4: Dev Agent
        logger.info("Step 4: Dev Agent")
        dev_result = await self.agents["dev"].execute({
            "task_type": "user_stories",
            "feature": input_data.get("feature", ""),
            "requirements": input_data.get("requirements", [])
        })
        results["steps"].append(dev_result)
        
        # Step 5: Prototype Agent
        logger.info("Step 5: Prototype Agent")
        prototype_result = await self.agents["prototype"].execute({
            "task_type": "mockup",
            "feature": input_data.get("feature", ""),
            "style": "modern"
        })
        results["steps"].append(prototype_result)
        
        # Step 6: GTM Agent
        logger.info("Step 6: GTM Agent")
        gtm_result = await self.agents["gtm"].execute({
            "task_type": "launch_plan",
            "product": input_data.get("feature", ""),
            "target_audience": input_data.get("audience", "Product Managers")
        })
        results["steps"].append(gtm_result)
        
        # Step 7: Automation Agent
        logger.info("Step 7: Automation Agent")
        automation_result = await self.agents["automation"].execute({
            "task_type": "workflow_automation",
            "automation_config": {"feature": input_data.get("feature", "")}
        })
        results["steps"].append(automation_result)
        
        # Step 8: Regulation Agent
        logger.info("Step 8: Regulation Agent")
        regulation_result = await self.agents["regulation"].execute({
            "task_type": "compliance_check",
            "feature": input_data.get("feature", ""),
            "jurisdiction": input_data.get("jurisdiction", "US")
        })
        results["steps"].append(regulation_result)
        
        # Step 9: Risk Assessment Agent
        logger.info("Step 9: Risk Assessment Agent")
        risk_result = await self.agents["risk_assessment"].execute({
            "task_type": "assess",
            "project_data": {"feature": input_data.get("feature", "")},
            "context": results
        })
        results["steps"].append(risk_result)
        
        # Step 10: PRD Agent - Synthesize everything into PRD
        logger.info("Step 10: PRD Agent - Generating final document")
        prd_result = await self.agents["prd"].execute({
            "workflow_results": results,
            "product_name": input_data.get("feature", "New Product"),
            "version": input_data.get("version", "1.0")
        })
        results["steps"].append(prd_result)
        results["prd"] = prd_result.get("result", {})
        
        # Generate summary
        results["summary"] = self._generate_workflow_summary(results["steps"])
        
        return results
    
    async def _research_and_strategy(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Research and Strategy workflow: Research → Strategy"""
        results = {"workflow": "research_and_strategy", "steps": []}
        
        # Research first
        research_result = await self.agents["research"].execute({
            "task_type": "user_research",
            "query": input_data.get("query", ""),
            "sources": input_data.get("sources", ["reddit", "twitter"])
        })
        results["steps"].append(research_result)
        
        # Then strategy
        strategy_result = await self.agents["strategy"].execute({
            "task_type": "competitive_analysis",
            "target_market": input_data.get("market", "")
        })
        results["steps"].append(strategy_result)
        
        results["summary"] = self._generate_workflow_summary(results["steps"])
        return results
    
    async def _dev_planning(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Dev planning workflow: Dev → Prototype"""
        results = {"workflow": "dev_planning", "steps": []}
        
        # Generate stories
        dev_result = await self.agents["dev"].execute({
            "task_type": "user_stories",
            "feature": input_data.get("feature", ""),
            "requirements": input_data.get("requirements", [])
        })
        results["steps"].append(dev_result)
        
        # Create prototypes
        prototype_result = await self.agents["prototype"].execute({
            "task_type": "wireframe",
            "feature": input_data.get("feature", "")
        })
        results["steps"].append(prototype_result)
        
        results["summary"] = self._generate_workflow_summary(results["steps"])
        return results
    
    async def _launch_planning(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Launch planning workflow: GTM → Automation"""
        results = {"workflow": "launch_planning", "steps": []}
        
        # GTM strategy
        gtm_result = await self.agents["gtm"].execute({
            "task_type": "launch_plan",
            "product": input_data.get("product", ""),
            "target_audience": input_data.get("audience", "")
        })
        results["steps"].append(gtm_result)
        
        # Automation setup
        automation_result = await self.agents["automation"].execute({
            "task_type": "workflow_automation",
            "automation_config": input_data
        })
        results["steps"].append(automation_result)
        
        results["summary"] = self._generate_workflow_summary(results["steps"])
        return results
    
    async def _compliance_check(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Compliance check workflow: Regulation only"""
        results = {"workflow": "compliance_check", "steps": []}
        
        regulation_result = await self.agents["regulation"].execute({
            "task_type": "compliance_check",
            "feature": input_data.get("feature", ""),
            "jurisdiction": input_data.get("jurisdiction", "US")
        })
        results["steps"].append(regulation_result)
        
        results["summary"] = self._generate_workflow_summary(results["steps"])
        return results
    
    async def _custom_workflow(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Execute custom workflow based on agent list"""
        results = {"workflow": "custom", "steps": []}
        
        agents_to_run = input_data.get("agents", ["strategy"])
        
        for agent_name in agents_to_run:
            if agent_name in self.agents:
                agent_result = await self.agents[agent_name].execute(
                    input_data.get("task_input", {})
                )
                results["steps"].append(agent_result)
        
        results["summary"] = self._generate_workflow_summary(results["steps"])
        return results
    
    def _generate_workflow_summary(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of workflow execution"""
        completed = sum(1 for step in steps if step.get("status") == "completed")
        failed = sum(1 for step in steps if step.get("status") == "failed")
        
        return {
            "total_steps": len(steps),
            "completed": completed,
            "failed": failed,
            "agents_used": [step.get("agent") for step in steps],
            "execution_time": "simulated",
            "key_outputs": [
                step.get("result", {}) 
                for step in steps 
                if step.get("status") == "completed"
            ]
        }
    
    def _store_workflow_memory(
        self,
        workflow_id: str,
        workflow_type: str,
        input_data: Dict[str, Any],
        result: Dict[str, Any],
        project_id: Optional[int]
    ):
        """Store workflow execution in memory"""
        memory_text = f"""
        Workflow: {workflow_type}
        Input: {input_data}
        Result: Completed with {result.get('summary', {}).get('completed', 0)} successful steps
        """
        
        memory_manager.add_memory(
            text=memory_text,
            metadata={
                "workflow_id": workflow_id,
                "workflow_type": workflow_type,
                "project_id": project_id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        self.workflow_history.append({
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "timestamp": datetime.now().isoformat(),
            "status": result.get("status", "unknown")
        })
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        return {
            agent_name: {
                "name": agent.name,
                "status": agent.status,
                "goal": agent.goal
            }
            for agent_name, agent in self.agents.items()
        }
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workflow history"""
        return self.workflow_history[-limit:]


# Global instance
task_graph = TaskGraph()

