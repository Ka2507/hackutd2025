"""
Adaptive Workflow Engine - Dynamic agent routing based on task analysis
Uses Nemotron to intelligently plan and adapt workflows
"""
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import asyncio
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .nemotron_bridge import nemotron_bridge
from .memory_manager import memory_manager
from utils.logger import logger


class WorkflowNode:
    """Represents a node in the adaptive workflow graph"""
    
    def __init__(self, agent_name: str, condition: Optional[Callable] = None):
        self.agent_name = agent_name
        self.condition = condition  # Function to determine if this node should execute
        self.dependencies = []  # Nodes that must complete before this
        self.parallel_group = None  # Nodes that can run in parallel
        self.quality_threshold = 0.7  # Minimum quality score to proceed
        self.result = None
        self.status = "pending"  # pending, running, completed, failed, skipped
        
    def can_execute(self, context: Dict[str, Any]) -> bool:
        """Check if this node can execute based on dependencies and conditions"""
        if self.condition and not self.condition(context):
            return False
        
        # Check if all dependencies are completed
        for dep in self.dependencies:
            if dep.status != "completed":
                return False
        
        return True


class AdaptiveWorkflowEngine:
    """
    Intelligent workflow engine that adapts based on context and results
    """
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.workflow_graph = []
        self.execution_history = []
        
    async def plan_workflow(
        self,
        task_description: str,
        input_data: Dict[str, Any],
        available_agents: List[str]
    ) -> List[WorkflowNode]:
        """
        Use Nemotron to intelligently plan the optimal workflow
        
        Args:
            task_description: High-level task description
            input_data: Input parameters
            available_agents: List of available agent names
            
        Returns:
            List of WorkflowNode objects representing the planned workflow
        """
        logger.info(f"Planning adaptive workflow for: {task_description}")
        
        # Check for similar past workflows
        similar_workflows = await self._find_similar_workflows(task_description)
        
        # Use Nemotron to analyze task and plan workflow
        planning_prompt = f"""
        Task: {task_description}
        
        Available Agents: {', '.join(available_agents)}
        
        Input Context: {input_data}
        
        Similar Past Workflows: {similar_workflows[:3] if similar_workflows else 'None'}
        
        Create an optimal workflow plan that:
        1. Identifies which agents are needed
        2. Determines the best execution sequence (sequential vs parallel)
        3. Identifies dependencies between agents
        4. Suggests quality thresholds for each step
        5. Plans for potential adaptations if quality is low
        
        Consider:
        - Can any agents run in parallel?
        - What information does each agent need from previous agents?
        - What are potential failure points and how to handle them?
        
        Provide a structured plan with agent sequence, dependencies, and execution strategy.
        """
        
        response = await nemotron_bridge.call_nemotron(
            prompt=planning_prompt,
            task_type="orchestration",
            priority="high",
            max_tokens=2000
        )
        
        # Parse Nemotron response into workflow nodes
        nodes = self._parse_workflow_plan(response["response"], available_agents, input_data)
        
        logger.info(f"Planned workflow with {len(nodes)} nodes")
        return nodes
    
    def _parse_workflow_plan(
        self,
        plan_text: str,
        available_agents: List[str],
        context: Dict[str, Any]
    ) -> List[WorkflowNode]:
        """
        Parse Nemotron's workflow plan into WorkflowNode objects
        
        This is a simplified parser - in production, use structured output
        """
        nodes = []
        plan_lower = plan_text.lower()
        
        # Extract agent sequence from plan
        # Look for agent names in the plan
        agent_sequence = []
        for agent in available_agents:
            if agent.lower() in plan_lower:
                agent_sequence.append(agent)
        
        # If Nemotron didn't provide clear sequence, use intelligent defaults
        if not agent_sequence:
            agent_sequence = self._default_agent_sequence(context)
        
        # Create nodes with dependencies
        for i, agent_name in enumerate(agent_sequence):
            node = WorkflowNode(agent_name=agent_name)
            
            # Set dependencies (previous agents)
            if i > 0:
                node.dependencies = [nodes[i-1]]
            
            # Check if this agent can run in parallel with previous
            if i > 0 and self._can_run_parallel(agent_name, agent_sequence[i-1]):
                node.parallel_group = nodes[i-1].parallel_group or f"parallel_{i-1}"
                nodes[i-1].parallel_group = node.parallel_group
            
            nodes.append(node)
        
        return nodes
    
    def _default_agent_sequence(self, context: Dict[str, Any]) -> List[str]:
        """Intelligent default sequence based on context"""
        task_type = context.get("task_type", "general")
        
        if "research" in task_type or "market" in task_type:
            return ["research", "strategy", "dev", "prototype", "gtm"]
        elif "development" in task_type or "backlog" in task_type:
            return ["dev", "prototype", "regulation"]
        elif "launch" in task_type or "gtm" in task_type:
            return ["gtm", "automation", "regulation"]
        else:
            return ["strategy", "research", "dev", "prototype", "gtm"]
    
    def _can_run_parallel(self, agent1: str, agent2: str) -> bool:
        """Check if two agents can run in parallel"""
        # Agents that can run in parallel (no dependencies)
        parallel_pairs = [
            ("research", "strategy"),  # Can research while strategizing
            ("prototype", "dev"),  # Can prototype while writing stories
            ("automation", "gtm"),  # Can automate while planning launch
        ]
        
        return (agent1, agent2) in parallel_pairs or (agent2, agent1) in parallel_pairs
    
    async def execute_adaptive_workflow(
        self,
        nodes: List[WorkflowNode],
        input_data: Dict[str, Any],
        shared_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow with adaptive behavior
        
        Args:
            nodes: List of workflow nodes to execute
            input_data: Initial input data
            shared_context: Shared context dictionary
            
        Returns:
            Workflow execution results
        """
        results = {
            "workflow_type": "adaptive",
            "nodes": [],
            "adaptations": [],
            "start_time": datetime.now().isoformat()
        }
        
        # Group nodes by parallel groups
        execution_groups = self._group_by_parallel(nodes)
        
        for group in execution_groups:
            if len(group) > 1:
                # Execute in parallel
                logger.info(f"Executing {len(group)} agents in parallel")
                group_results = await asyncio.gather(*[
                    self._execute_node(node, input_data, shared_context)
                    for node in group
                ])
                
                for node, result in zip(group, group_results):
                    node.result = result
                    results["nodes"].append({
                        "agent": node.agent_name,
                        "status": node.status,
                        "result": result
                    })
            else:
                # Execute sequentially
                node = group[0]
                if node.can_execute(shared_context):
                    result = await self._execute_node(node, input_data, shared_context)
                    node.result = result
                    results["nodes"].append({
                        "agent": node.agent_name,
                        "status": node.status,
                        "result": result
                    })
                    
                    # Check quality and adapt if needed
                    if node.status == "completed" and result.get("quality_score", 1.0) < node.quality_threshold:
                        adaptation = await self._adapt_workflow(node, result, shared_context)
                        if adaptation:
                            results["adaptations"].append(adaptation)
                            # Re-execute with adaptation
                            result = await self._execute_node(node, input_data, shared_context)
                            node.result = result
        
        results["end_time"] = datetime.now().isoformat()
        results["summary"] = self._generate_summary(results["nodes"])
        
        return results
    
    async def _execute_node(
        self,
        node: WorkflowNode,
        input_data: Dict[str, Any],
        shared_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single workflow node"""
        node.status = "running"
        logger.info(f"Executing node: {node.agent_name}")
        
        try:
            agent = self.agents[node.agent_name]
            
            # Prepare input with context from previous nodes
            task_input = {
                **input_data,
                "context_from_previous": self._extract_relevant_context(node, shared_context)
            }
            
            result = await agent.execute(task_input)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(result)
            result["quality_score"] = quality_score
            
            # Update shared context
            shared_context[f"{node.agent_name}_output"] = result
            shared_context[f"{node.agent_name}_quality"] = quality_score
            
            node.status = "completed" if quality_score >= node.quality_threshold else "completed_low_quality"
            
            return result
            
        except Exception as e:
            logger.error(f"Node {node.agent_name} failed: {e}")
            node.status = "failed"
            return {
                "error": str(e),
                "quality_score": 0.0,
                "status": "failed"
            }
    
    def _extract_relevant_context(self, node: WorkflowNode, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant context from previous nodes for this agent"""
        context = {}
        
        for dep in node.dependencies:
            if dep.result:
                # Extract relevant parts of previous result
                context[dep.agent_name] = {
                    "key_insights": dep.result.get("result", {}).get("insights", []),
                    "outputs": dep.result.get("result", {}),
                    "quality": dep.result.get("quality_score", 1.0)
                }
        
        return context
    
    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate quality score for agent output"""
        score = 1.0
        
        # Check for errors
        if result.get("error"):
            return 0.0
        
        # Check result completeness
        result_data = result.get("result", {})
        if not result_data:
            score -= 0.3
        
        # Check for key fields
        if "status" in result and result["status"] == "failed":
            score -= 0.5
        
        # Check result richness (more data = higher quality)
        if isinstance(result_data, dict):
            if len(result_data) < 3:
                score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    async def _adapt_workflow(
        self,
        node: WorkflowNode,
        result: Dict[str, Any],
        shared_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Adapt workflow when quality is low"""
        logger.info(f"Adapting workflow for {node.agent_name} (quality: {result.get('quality_score', 0)})")
        
        # Use Nemotron to suggest adaptation
        adaptation_prompt = f"""
        Agent {node.agent_name} produced output with quality score {result.get('quality_score', 0)}.
        
        Output: {result.get('result', {})}
        
        Suggest how to improve this output:
        1. Should we re-run with different parameters?
        2. Should we use a different agent?
        3. Should we gather more context first?
        
        Provide specific adaptation strategy.
        """
        
        adaptation_response = await nemotron_bridge.call_nemotron(
            prompt=adaptation_prompt,
            task_type="orchestration",
            priority="medium",
            max_tokens=500
        )
        
        return {
            "node": node.agent_name,
            "original_quality": result.get("quality_score", 0),
            "adaptation_strategy": adaptation_response["response"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _group_by_parallel(self, nodes: List[WorkflowNode]) -> List[List[WorkflowNode]]:
        """Group nodes that can execute in parallel"""
        groups = []
        current_group = []
        current_parallel_id = None
        
        for node in nodes:
            if node.parallel_group and node.parallel_group == current_parallel_id:
                current_group.append(node)
            else:
                if current_group:
                    groups.append(current_group)
                current_group = [node]
                current_parallel_id = node.parallel_group
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    async def _find_similar_workflows(self, task_description: str) -> List[Dict[str, Any]]:
        """Find similar past workflows using semantic search"""
        # Search memory for similar workflows
        similar = memory_manager.search(
            query=task_description,
            top_k=5,
            filter_metadata={"type": "workflow"}
        )
        
        return [mem["metadata"] for mem in similar]
    
    def _generate_summary(self, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate workflow execution summary"""
        completed = sum(1 for n in nodes if n["status"] == "completed")
        failed = sum(1 for n in nodes if n["status"] == "failed")
        avg_quality = sum(n.get("result", {}).get("quality_score", 0) for n in nodes) / len(nodes) if nodes else 0
        
        return {
            "total_nodes": len(nodes),
            "completed": completed,
            "failed": failed,
            "average_quality": avg_quality,
            "adaptations": len([n for n in nodes if "adaptation" in n])
        }

