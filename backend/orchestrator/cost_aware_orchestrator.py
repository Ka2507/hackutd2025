"""
Cost-Aware Orchestrator - Intelligently manages API budget
Maximizes value per API call while staying within $40 budget
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import logger


class TaskValue(Enum):
    """Task value levels for cost optimization"""
    CRITICAL = 1.0  # Must use Nemotron
    HIGH = 0.8     # Should use Nemotron
    MEDIUM = 0.5   # Consider Nemotron
    LOW = 0.2      # Use local LLM
    FORMATTING = 0.1  # Never use Nemotron


class CostAwareOrchestrator:
    """
    Manages API budget intelligently by:
    1. Assigning value scores to tasks
    2. Batching similar tasks
    3. Caching aggressively
    4. Forecasting budget usage
    """
    
    def __init__(self, total_budget: float = 40.0):
        self.total_budget = total_budget
        self.used_budget = 0.0
        self.budget_history = []
        self.task_value_cache = {}
        
        # Estimated costs (in dollars)
        self.nemotron_cost_per_1k_tokens = 0.002  # Approximate
        self.avg_tokens_per_call = 2000  # Average tokens per Nemotron call
        
    def should_use_nemotron(
        self,
        task_type: str,
        task_description: str,
        context: Dict[str, Any]
    ) -> Tuple[bool, float]:
        """
        Determine if task should use Nemotron
        
        Returns:
            (should_use, value_score)
        """
        # Calculate task value
        value_score = self._calculate_task_value(task_type, task_description, context)
        
        # Check budget
        remaining_budget = self.total_budget - self.used_budget
        budget_ratio = remaining_budget / self.total_budget
        
        # Decision logic
        if value_score >= TaskValue.HIGH.value:
            # High-value tasks: use Nemotron if budget allows
            if budget_ratio > 0.3:  # At least 30% budget remaining
                return True, value_score
            elif budget_ratio > 0.1 and value_score >= TaskValue.CRITICAL.value:
                # Critical tasks even with low budget
                return True, value_score
            else:
                logger.warning(f"High-value task {task_type} skipped due to budget constraints")
                return False, value_score
        
        elif value_score >= TaskValue.MEDIUM.value:
            # Medium-value: use if budget is healthy
            if budget_ratio > 0.5:
                return True, value_score
            else:
                return False, value_score
        
        else:
            # Low-value: never use Nemotron
            return False, value_score
    
    def _calculate_task_value(
        self,
        task_type: str,
        task_description: str,
        context: Dict[str, Any]
    ) -> float:
        """Calculate value score for a task"""
        
        # Check cache
        cache_key = f"{task_type}_{hash(task_description[:50])}"
        if cache_key in self.task_value_cache:
            return self.task_value_cache[cache_key]
        
        # High-value task types
        high_value_types = [
            "orchestration",
            "strategic_planning",
            "risk_analysis",
            "prioritization",
            "complex_reasoning",
            "multi_agent_coordination",
            # Agent-specific task types (all high-value)
            "launch_plan",
            "marketing_strategy",
            "pricing",
            "messaging",
            "gtm",
            "idea_generation",
            "competitive_analysis",
            "user_research",
            "user_stories",
            "backlog",
            "mockup",
            "design",
            "compliance_check",
            "regulation",
            "workflow_automation"
        ]
        
        # Medium-value task types
        medium_value_types = [
            "market_sizing",
            "user_research_synthesis",
            "research",
            "analysis"
        ]
        
        # Low-value task types
        low_value_types = [
            "formatting",
            "simple_extraction",
            "data_aggregation",
            "template_filling"
        ]
        
        # Determine base value
        if task_type in high_value_types:
            base_value = TaskValue.HIGH.value
        elif task_type in medium_value_types:
            base_value = TaskValue.MEDIUM.value
        elif task_type in low_value_types:
            base_value = TaskValue.LOW.value
        else:
            base_value = TaskValue.MEDIUM.value
        
        # Adjust based on context
        adjustments = 0.0
        
        # If task affects multiple agents, increase value
        if context.get("affects_multiple_agents", False):
            adjustments += 0.1
        
        # If task is time-sensitive, increase value
        if context.get("time_sensitive", False):
            adjustments += 0.1
        
        # If task has high impact on final output, increase value
        if context.get("high_impact", False):
            adjustments += 0.15
        
        # If similar task was cached, decrease value (can use cache)
        if self._has_similar_cached_task(task_description):
            adjustments -= 0.2
        
        final_value = min(1.0, base_value + adjustments)
        
        # Cache result
        self.task_value_cache[cache_key] = final_value
        
        return final_value
    
    def _has_similar_cached_task(self, task_description: str) -> bool:
        """Check if similar task was recently cached"""
        # Simplified check - in production, use semantic similarity
        return False
    
    async def batch_similar_tasks(
        self,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch similar tasks into single Nemotron call
        
        Args:
            tasks: List of tasks to batch
            
        Returns:
            Batched response
        """
        if not tasks:
            return {}
        
        # Group tasks by similarity
        groups = self._group_similar_tasks(tasks)
        
        results = {}
        for group in groups:
            if len(group) == 1:
                # Single task, process normally
                task = group[0]
                should_use, value = self.should_use_nemotron(
                    task["task_type"],
                    task["description"],
                    task.get("context", {})
                )
                
                if should_use:
                    result = await self._process_with_nemotron(task)
                    results[task["id"]] = result
                else:
                    result = await self._process_locally(task)
                    results[task["id"]] = result
            else:
                # Batch process
                batched_prompt = self._create_batched_prompt(group)
                result = await nemotron_bridge.call_nemotron(
                    prompt=batched_prompt,
                    task_type="batch_processing",
                    priority="medium",
                    max_tokens=3000
                )
                
                # Split results
                split_results = self._split_batched_results(result, group)
                results.update(split_results)
                
                # Track cost
                self._track_cost(result)
        
        return results
    
    def _group_similar_tasks(self, tasks: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group tasks by similarity for batching"""
        groups = []
        
        # Simple grouping by task type
        type_groups = {}
        for task in tasks:
            task_type = task.get("task_type", "general")
            if task_type not in type_groups:
                type_groups[task_type] = []
            type_groups[task_type].append(task)
        
        # Create groups (max 3 tasks per batch to maintain quality)
        for task_type, type_tasks in type_groups.items():
            for i in range(0, len(type_tasks), 3):
                groups.append(type_tasks[i:i+3])
        
        return groups
    
    def _create_batched_prompt(self, tasks: List[Dict[str, Any]]) -> str:
        """Create a single prompt for multiple tasks"""
        prompt_parts = [
            "Process the following tasks in a single response:",
            ""
        ]
        
        for i, task in enumerate(tasks, 1):
            prompt_parts.append(f"Task {i}: {task.get('description', '')}")
            prompt_parts.append(f"Type: {task.get('task_type', 'general')}")
            if task.get("context"):
                prompt_parts.append(f"Context: {task.get('context')}")
            prompt_parts.append("")
        
        prompt_parts.append("Provide structured responses for each task, clearly labeled.")
        
        return "\n".join(prompt_parts)
    
    def _split_batched_results(
        self,
        batched_result: Dict[str, Any],
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Split batched Nemotron response into individual results"""
        response_text = batched_result.get("response", "")
        results = {}
        
        # Simple splitting - in production, use structured output
        for i, task in enumerate(tasks):
            # Try to extract task-specific response
            task_id = task.get("id", f"task_{i}")
            results[task_id] = {
                "response": response_text,  # Full response for now
                "task_id": task_id,
                "batched": True
            }
        
        return results
    
    async def _process_with_nemotron(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with Nemotron"""
        result = await nemotron_bridge.call_nemotron(
            prompt=task.get("description", ""),
            task_type=task.get("task_type", "general"),
            priority="high" if task.get("value_score", 0) > 0.7 else "medium",
            max_tokens=2000
        )
        
        self._track_cost(result)
        return result
    
    async def _process_locally(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with local LLM (fallback)"""
        logger.info(f"Processing {task.get('task_type')} locally to save budget")
        
        # Simulate local processing
        return {
            "response": f"Local processing result for {task.get('description', 'task')}",
            "model": "local_fallback",
            "usage": {"total_tokens": 0},
            "timestamp": datetime.now().isoformat(),
            "note": "Processed locally to conserve Nemotron budget"
        }
    
    def _track_cost(self, result: Dict[str, Any]):
        """Track API cost"""
        usage = result.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        
        # Estimate cost
        cost = (total_tokens / 1000) * self.nemotron_cost_per_1k_tokens
        self.used_budget += cost
        
        self.budget_history.append({
            "timestamp": datetime.now().isoformat(),
            "tokens": total_tokens,
            "cost": cost,
            "remaining_budget": self.total_budget - self.used_budget
        })
        
        logger.info(f"Budget used: ${self.used_budget:.2f} / ${self.total_budget:.2f}")
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status"""
        remaining = self.total_budget - self.used_budget
        percentage_used = (self.used_budget / self.total_budget) * 100
        
        # Forecast remaining budget
        avg_cost_per_call = self.used_budget / len(self.budget_history) if self.budget_history else 0
        estimated_remaining_calls = remaining / avg_cost_per_call if avg_cost_per_call > 0 else 0
        
        return {
            "total_budget": self.total_budget,
            "used_budget": round(self.used_budget, 2),
            "remaining_budget": round(remaining, 2),
            "percentage_used": round(percentage_used, 1),
            "estimated_remaining_calls": round(estimated_remaining_calls, 1),
            "budget_status": self._get_budget_status_level(percentage_used),
            "recommendations": self._get_budget_recommendations(percentage_used)
        }
    
    def _get_budget_status_level(self, percentage_used: float) -> str:
        """Get budget status level"""
        if percentage_used >= 90:
            return "critical"
        elif percentage_used >= 75:
            return "warning"
        elif percentage_used >= 50:
            return "moderate"
        else:
            return "healthy"
    
    def _get_budget_recommendations(self, percentage_used: float) -> List[str]:
        """Get recommendations based on budget usage"""
        recommendations = []
        
        if percentage_used >= 90:
            recommendations.append("Budget critical! Use local LLM for all non-critical tasks")
            recommendations.append("Aggressively cache responses")
        elif percentage_used >= 75:
            recommendations.append("Budget getting low - prioritize high-value tasks only")
            recommendations.append("Consider batching remaining tasks")
        elif percentage_used >= 50:
            recommendations.append("Budget at 50% - continue smart allocation")
        else:
            recommendations.append("Budget healthy - can use Nemotron for high-value tasks")
        
        return recommendations
    
    def forecast_budget(self, planned_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Forecast budget usage for planned tasks"""
        estimated_cost = 0.0
        high_value_tasks = 0
        
        for task in planned_tasks:
            should_use, value = self.should_use_nemotron(
                task.get("task_type", "general"),
                task.get("description", ""),
                task.get("context", {})
            )
            
            if should_use:
                estimated_cost += (self.avg_tokens_per_call / 1000) * self.nemotron_cost_per_1k_tokens
                if value >= TaskValue.HIGH.value:
                    high_value_tasks += 1
        
        remaining_after = self.total_budget - self.used_budget - estimated_cost
        
        return {
            "estimated_cost": round(estimated_cost, 2),
            "remaining_after": round(remaining_after, 2),
            "high_value_tasks": high_value_tasks,
            "feasible": remaining_after >= 0,
            "recommendation": "Proceed" if remaining_after >= 0 else "Reduce scope or use local LLM for some tasks"
        }

