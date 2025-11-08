"""
Strategy Agent - Handles market sizing, idea generation, and strategic planning
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class StrategyAgent(BaseAgent):
    """Agent specialized in strategic planning and market analysis"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="StrategyAgent",
            goal="Provide strategic insights, market sizing, and idea generation",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategy-related tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "market_sizing", "idea_generation", "competitive_analysis"
                - product_idea: Product concept (optional)
                - target_market: Target market segment (optional)
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "idea_generation")
        product_idea = task_input.get("product_idea", "")
        target_market = task_input.get("target_market", "")
        
        try:
            if task_type == "market_sizing":
                result = await self._market_sizing(target_market)
            elif task_type == "idea_generation":
                result = await self._idea_generation(product_idea)
            elif task_type == "competitive_analysis":
                result = await self._competitive_analysis(target_market)
            else:
                result = await self._strategic_planning(task_input)
            
            # Store insights in shared context
            self.update_context("strategy_insights", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _market_sizing(self, market: str) -> Dict[str, Any]:
        """Perform market sizing analysis"""
        prompt = f"Analyze the market size and opportunity for: {market}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "market": market,
            "tam": "$50B",
            "sam": "$5B",
            "som": "$500M",
            "analysis": llm_response,
            "growth_rate": "15% CAGR",
            "key_trends": [
                "AI adoption accelerating",
                "Product teams seeking automation",
                "Integration with existing tools critical"
            ]
        }
    
    async def _idea_generation(self, idea: str) -> Dict[str, Any]:
        """Generate and refine product ideas"""
        prompt = f"Expand and refine this product idea: {idea}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "original_idea": idea,
            "refined_concept": llm_response,
            "value_propositions": [
                "Save 10+ hours per week on PM tasks",
                "AI-powered insights for better decisions",
                "Seamless integration with existing tools"
            ],
            "target_personas": [
                "Senior Product Managers at mid-size tech companies",
                "Product Leaders managing multiple teams",
                "Solo founders wearing PM hats"
            ],
            "differentiators": [
                "Multi-agent reasoning system",
                "Local-first AI for privacy",
                "Nemotron-powered strategic planning"
            ]
        }
    
    async def _competitive_analysis(self, market: str) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        prompt = f"Analyze competitors in: {market}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "market": market,
            "competitors": [
                {
                    "name": "ProductBoard",
                    "strengths": ["Feature prioritization", "User feedback"],
                    "weaknesses": ["No AI agents", "Limited automation"]
                },
                {
                    "name": "Aha!",
                    "strengths": ["Roadmapping", "Strategy tools"],
                    "weaknesses": ["Complex UI", "No AI reasoning"]
                },
                {
                    "name": "Linear",
                    "strengths": ["Developer-friendly", "Fast"],
                    "weaknesses": ["PM tools limited", "No AI copilot"]
                }
            ],
            "market_gaps": [
                "No true AI agent orchestration",
                "Limited multi-step reasoning",
                "Poor integration between planning and execution"
            ],
            "positioning": llm_response
        }
    
    async def _strategic_planning(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """General strategic planning"""
        prompt = f"Create strategic plan for: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "strategic_pillars": [
                "AI-First Product Management",
                "Workflow Automation",
                "Data-Driven Insights"
            ],
            "success_metrics": [
                "Time saved per PM per week",
                "Decision quality improvement",
                "User adoption rate"
            ],
            "plan": llm_response
        }

