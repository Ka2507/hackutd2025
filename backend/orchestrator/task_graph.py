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
    RiskAssessmentAgent, PrioritizationAgent
)
from agents.agent_config import get_agents_in_lifecycle_order, get_agent_stage
from .memory_manager import memory_manager
from .nemotron_bridge import nemotron_bridge
from .adaptive_workflow import AdaptiveWorkflowEngine
from .agent_collaboration import AgentCollaboration
from utils.logger import logger


class WorkflowType(Enum):
    """Predefined workflow types"""
    FULL_FEATURE_PLANNING = "full_feature_planning"
    RESEARCH_AND_STRATEGY = "research_and_strategy"
    DEV_PLANNING = "dev_planning"
    LAUNCH_PLANNING = "launch_planning"
    COMPLIANCE_CHECK = "compliance_check"
    ADAPTIVE = "adaptive"  # New: Adaptive workflow
    CUSTOM = "custom"


class TaskGraph:
    """
    Orchestrates multi-agent workflows using a graph-based approach
    Similar to LangGraph but simplified for MVP
    """
    
    def __init__(self):
        """Initialize task graph with all agents ordered by Product Management Lifecycle"""
        self.shared_context = {}
        
        # Initialize all agents
        agent_instances = {
            "strategy": StrategyAgent(self.shared_context),
            "research": ResearchAgent(self.shared_context),
            "prioritization": PrioritizationAgent(self.shared_context),
            "risk": RiskAssessmentAgent(self.shared_context),
            "regulation": RegulationAgent(self.shared_context),
            "dev": DevAgent(self.shared_context),
            "prototype": PrototypeAgent(self.shared_context),
            "gtm": GtmAgent(self.shared_context),
            "automation": AutomationAgent(self.shared_context),
        }
        
        # Order agents by Product Management Lifecycle
        lifecycle_order = get_agents_in_lifecycle_order()
        self.agents = {key: agent_instances[key] for key in lifecycle_order if key in agent_instances}
        
        # Store lifecycle order for reference
        self.lifecycle_order = lifecycle_order
        
        self.workflow_history = []
        self.adaptive_engine = AdaptiveWorkflowEngine(self.agents)
        self.collaboration = AgentCollaboration(self.agents)
        
        logger.info("TaskGraph initialized with agents ordered by Product Management Lifecycle:")
        for i, agent_key in enumerate(lifecycle_order, 1):
            if agent_key in self.agents:
                agent = self.agents[agent_key]
                logger.info(f"  {i}. {agent.name} - Stage {agent.lifecycle_stage}: {agent.stage_name} (Model: {agent.nemotron_model})")
    
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
            WorkflowType.ADAPTIVE.value: self._adaptive_workflow,
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
        Full feature planning workflow:
        Strategy → Research → Dev → Prototype → GTM → Automation → Regulation
        """
        results = {"workflow": "full_feature_planning", "steps": []}
        
        # Step 1: Strategy Agent - Market analysis and idea generation
        logger.info("Step 1: Strategy Agent")
        strategy_result = await self.agents["strategy"].execute({
            "task_type": "idea_generation",
            "product_idea": input_data.get("feature", ""),
            "target_market": input_data.get("market", "")
        })
        results["steps"].append(strategy_result)
        
        # Step 2: Research Agent - User research and competitive analysis
        logger.info("Step 2: Research Agent")
        research_result = await self.agents["research"].execute({
            "task_type": "user_research",
            "query": input_data.get("feature", ""),
            "sources": ["reddit", "twitter", "product_hunt"]
        })
        results["steps"].append(research_result)
        
        # Step 2.5: Risk Assessment - Early risk detection
        logger.info("Step 2.5: Risk Assessment")
        current_state = {
            "feature": input_data.get("feature", ""),
            "market": input_data.get("market", ""),
            "strategy_output": strategy_result.get("result", {}),
            "research_output": research_result.get("result", {})
        }
        risk_result = await self.agents["risk"].execute({
            "workflow_state": current_state,
            "project_id": project_id
        })
        results["steps"].append(risk_result)
        
        # Step 3: Dev Agent - Generate user stories and backlog
        logger.info("Step 3: Dev Agent")
        dev_result = await self.agents["dev"].execute({
            "task_type": "user_stories",
            "feature": input_data.get("feature", ""),
            "requirements": input_data.get("requirements", [])
        })
        results["steps"].append(dev_result)
        
        # Step 3.5: Prioritization - Smart prioritization of generated stories
        logger.info("Step 3.5: Prioritization Agent")
        if dev_result.get("result", {}).get("stories"):
            stories = dev_result["result"]["stories"]
            prioritization_result = await self.agents["prioritization"].execute({
                "features": stories,
                "context": {
                    "market_data": strategy_result.get("result", {}),
                    "user_feedback": research_result.get("result", {}),
                    "strategic_goals": input_data.get("strategic_goals", [])
                },
                "method": "multi_factor"
            })
            results["steps"].append(prioritization_result)
            
            # Update dev_result with prioritized stories
            if prioritization_result.get("result", {}).get("prioritized_features"):
                dev_result["result"]["prioritized_stories"] = prioritization_result["result"]["prioritized_features"]
        
        # Step 4: Prototype Agent - Create mockups
        logger.info("Step 4: Prototype Agent")
        prototype_result = await self.agents["prototype"].execute({
            "task_type": "mockup",
            "feature": input_data.get("feature", ""),
            "style": "modern"
        })
        results["steps"].append(prototype_result)
        
        # Step 5: GTM Agent - Launch planning
        logger.info("Step 5: GTM Agent")
        gtm_result = await self.agents["gtm"].execute({
            "task_type": "launch_plan",
            "product": input_data.get("feature", ""),
            "target_audience": input_data.get("audience", "Product Managers")
        })
        results["steps"].append(gtm_result)
        
        # Step 6: Automation Agent - Setup automation
        logger.info("Step 6: Automation Agent")
        automation_result = await self.agents["automation"].execute({
            "task_type": "workflow_automation",
            "automation_config": {"feature": input_data.get("feature", "")}
        })
        results["steps"].append(automation_result)
        
        # Step 7: Regulation Agent - Compliance check
        logger.info("Step 7: Regulation Agent")
        regulation_result = await self.agents["regulation"].execute({
            "task_type": "compliance_check",
            "feature": input_data.get("feature", ""),
            "jurisdiction": input_data.get("jurisdiction", "US")
        })
        results["steps"].append(regulation_result)
        
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
        
        # Extract key information from each step
        key_outputs = []
        agents_used = []
        
        for step in steps:
            agent_name = step.get("agent", "Unknown")
            agents_used.append(agent_name)
            
            step_result = step.get("result", {})
            if step.get("status") == "completed" and step_result:
                # Extract meaningful content from agent result
                if isinstance(step_result, dict):
                    # Try to get the main content/analysis
                    content = step_result.get("launch_plan") or \
                             step_result.get("marketing_strategy") or \
                             step_result.get("strategic_analysis") or \
                             step_result.get("research_synthesis") or \
                             step_result.get("output") or \
                             step_result.get("raw_response") or \
                             str(step_result)[:500]  # Fallback to string representation
                    
                    key_outputs.append({
                        "agent": agent_name,
                        "summary": content[:1000] if isinstance(content, str) else str(content)[:1000],
                        "full_result": step_result
                    })
                else:
                    key_outputs.append({
                        "agent": agent_name,
                        "summary": str(step_result)[:500]
                    })
        
        return {
            "total_steps": len(steps),
            "completed": completed,
            "failed": failed,
            "agents_used": list(set(agents_used)),  # Remove duplicates
            "execution_time": "completed",
            "key_outputs": key_outputs,
            "summary_text": f"Workflow completed with {completed} successful steps and {failed} failures."
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
    
    async def _adaptive_workflow(
        self,
        input_data: Dict[str, Any],
        project_id: Optional[int]
    ) -> Dict[str, Any]:
        """Execute adaptive workflow using intelligent routing"""
        logger.info("Executing adaptive workflow")
        
        # Plan workflow dynamically
        task_description = input_data.get("task_description", input_data.get("feature", "General PM task"))
        nodes = await self.adaptive_engine.plan_workflow(
            task_description=task_description,
            input_data=input_data,
            available_agents=list(self.agents.keys())
        )
        
        # Execute with adaptation
        result = await self.adaptive_engine.execute_adaptive_workflow(
            nodes=nodes,
            input_data=input_data,
            shared_context=self.shared_context
        )
        
        # Convert to standard format
        return {
            "workflow": "adaptive",
            "steps": result.get("nodes", []),
            "nodes": result.get("nodes", []),  # Also include as nodes for consistency
            "adaptations": result.get("adaptations", []),
            "summary": result.get("summary", {}),
            "agents_used": [node.get("agent", "") for node in result.get("nodes", []) if node.get("agent")]
        }


# Global instance
task_graph = TaskGraph()

