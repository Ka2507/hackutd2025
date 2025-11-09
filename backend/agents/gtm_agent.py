"""
GTM Agent - Crafts go-to-market and launch plans
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class GtmAgent(BaseAgent):
    """Agent specialized in go-to-market strategy and launch planning"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="GtmAgent",
            goal="Create comprehensive go-to-market and launch strategies",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute GTM-related tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "launch_plan", "marketing_strategy", "pricing"
                - product: Product name/description
                - target_audience: Target audience details
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "launch_plan")
        product = task_input.get("product", "ProdPlex")
        target_audience = task_input.get("target_audience", "Product Managers")
        
        try:
            if task_type == "launch_plan":
                result = await self._create_launch_plan(product, target_audience)
            elif task_type == "marketing_strategy":
                result = await self._marketing_strategy(product, target_audience)
            elif task_type == "pricing":
                result = await self._pricing_strategy(product)
            elif task_type == "messaging":
                result = await self._create_messaging(product, target_audience)
            else:
                result = await self._general_gtm(task_input)
            
            self.update_context("gtm_strategy", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _create_launch_plan(self, product: str, audience: str) -> Dict[str, Any]:
        """Create comprehensive launch plan"""
        prompt = f"Create launch plan for {product} targeting {audience}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "product": product,
            "target_audience": audience,
            "launch_phases": [
                {
                    "phase": "Pre-Launch (Week -4 to -1)",
                    "activities": [
                        "Beta program with 50 PMs",
                        "Create demo videos and documentation",
                        "Build email waitlist",
                        "Prepare Product Hunt launch",
                        "Line up early customer testimonials"
                    ],
                    "goals": ["100+ beta signups", "5 customer interviews"],
                    "channels": ["LinkedIn", "Product Hunt", "PM communities"]
                },
                {
                    "phase": "Launch Week",
                    "activities": [
                        "Product Hunt launch (aim for #1)",
                        "LinkedIn campaign from founders",
                        "Email to waitlist",
                        "Post in PM Slack communities",
                        "Reddit r/ProductManagement post"
                    ],
                    "goals": ["1000+ signups", "Top 5 on Product Hunt"],
                    "channels": ["Product Hunt", "LinkedIn", "Email", "Reddit"]
                },
                {
                    "phase": "Post-Launch (Week 1-4)",
                    "activities": [
                        "Content marketing - blog posts",
                        "Customer success outreach",
                        "Collect and implement feedback",
                        "Referral program launch",
                        "Case study development"
                    ],
                    "goals": ["5000+ users", "20% activation rate"],
                    "channels": ["Blog", "Social", "Email", "Community"]
                }
            ],
            "launch_strategy": llm_response,
            "success_metrics": {
                "primary": ["User signups", "Activation rate", "Retention"],
                "secondary": ["Social mentions", "Press coverage", "Community engagement"]
            },
            "budget_allocation": {
                "paid_ads": "$500",
                "tools_and_software": "$200",
                "content_creation": "$300",
                "contingency": "$100"
            }
        }
    
    async def _marketing_strategy(self, product: str, audience: str) -> Dict[str, Any]:
        """Create marketing strategy"""
        prompt = f"Create marketing strategy for {product}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "product": product,
            "positioning": "The AI Copilot for Product Managers",
            "value_propositions": [
                "Save 10+ hours per week on PM tasks",
                "AI-powered multi-agent reasoning",
                "Privacy-first with local LLM",
                "Seamless workflow automation"
            ],
            "marketing_channels": [
                {
                    "channel": "Content Marketing",
                    "tactics": [
                        "Weekly blog posts on PM best practices",
                        "AI + PM thought leadership",
                        "Case studies and success stories"
                    ],
                    "priority": "High",
                    "budget": "$500/month"
                },
                {
                    "channel": "Community",
                    "tactics": [
                        "Active in PM Slack groups",
                        "Reddit r/ProductManagement presence",
                        "LinkedIn PM groups",
                        "Host monthly PM webinars"
                    ],
                    "priority": "High",
                    "budget": "$200/month"
                },
                {
                    "channel": "Product-Led Growth",
                    "tactics": [
                        "Freemium tier",
                        "In-app referral program",
                        "Usage-based expansion"
                    ],
                    "priority": "Critical",
                    "budget": "$0"
                },
                {
                    "channel": "Partnerships",
                    "tactics": [
                        "Integration partnerships (Jira, Slack)",
                        "PM tool ecosystem plays",
                        "Co-marketing with complementary tools"
                    ],
                    "priority": "Medium",
                    "budget": "$300/month"
                }
            ],
            "messaging_framework": {
                "hero_message": "Your AI Co-Pilot for Product Management",
                "sub_message": "Multi-agent AI that plans, researches, and automates PM workflows",
                "call_to_action": "Start Free Trial"
            },
            "strategy_details": llm_response
        }
    
    async def _pricing_strategy(self, product: str) -> Dict[str, Any]:
        """Create pricing strategy"""
        prompt = f"Design pricing strategy for {product}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "product": product,
            "pricing_model": "Freemium + Usage-based",
            "tiers": [
                {
                    "name": "Free",
                    "price": "$0/month",
                    "features": [
                        "Up to 3 projects",
                        "Basic agent tasks (10/month)",
                        "Local LLM only",
                        "Community support"
                    ],
                    "target": "Individual PMs, hobbyists"
                },
                {
                    "name": "Pro",
                    "price": "$49/month",
                    "features": [
                        "Unlimited projects",
                        "Unlimited agent tasks",
                        "Nemotron reasoning (50 calls/month)",
                        "All integrations",
                        "Priority support",
                        "Advanced analytics"
                    ],
                    "target": "Professional PMs"
                },
                {
                    "name": "Team",
                    "price": "$199/month (up to 5 users)",
                    "features": [
                        "Everything in Pro",
                        "Shared workspaces",
                        "Team collaboration",
                        "Advanced Nemotron (200 calls/month)",
                        "SSO",
                        "Dedicated support"
                    ],
                    "target": "Product teams"
                },
                {
                    "name": "Enterprise",
                    "price": "Custom",
                    "features": [
                        "Everything in Team",
                        "Unlimited users",
                        "On-premise deployment option",
                        "Custom integrations",
                        "SLA guarantee",
                        "White-glove onboarding"
                    ],
                    "target": "Large organizations"
                }
            ],
            "pricing_psychology": {
                "anchor": "Pro tier as primary recommendation",
                "value_metric": "Time saved per month",
                "roi_message": "Pay for itself in 2 hours saved"
            },
            "competitive_positioning": "20% below ProductBoard, 30% below Aha!",
            "strategy_rationale": llm_response
        }
    
    async def _create_messaging(self, product: str, audience: str) -> Dict[str, Any]:
        """Create messaging framework"""
        prompt = f"Create messaging for {product} targeting {audience}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "product": product,
            "target_audience": audience,
            "core_messages": {
                "headline": "Your AI Co-Pilot for Product Management",
                "tagline": "Plan. Research. Execute. Automate.",
                "elevator_pitch": "ProdPlex uses multi-agent AI to help Product Managers save 10+ hours per week on planning, research, and workflow automation."
            },
            "benefits_hierarchy": [
                "Time savings (quantified)",
                "Better decisions with AI insights",
                "Seamless automation",
                "Privacy with local AI"
            ],
            "proof_points": [
                "Multi-agent reasoning with NVIDIA Nemotron",
                "7 specialized AI agents",
                "Integrates with your existing tools",
                "Local-first for data privacy"
            ],
            "messaging_details": llm_response
        }
    
    async def _general_gtm(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general GTM tasks"""
        prompt = f"Execute GTM task: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "task": task_input,
            "output": llm_response
        }

