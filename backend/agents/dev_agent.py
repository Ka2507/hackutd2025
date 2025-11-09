"""
Dev Agent - Generates Jira stories, backlog items, and technical specs
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DevAgent(BaseAgent):
    """Agent specialized in generating development artifacts"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="DevAgent",
            goal="Generate user stories, backlog items, and technical specifications",
            context=context,
            agent_key="dev"
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute development-related tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "user_stories", "backlog", "tech_spec", "sprint_planning"
                - feature: Feature description
                - requirements: List of requirements
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "user_stories")
        feature = task_input.get("feature", "")
        requirements = task_input.get("requirements", [])
        
        try:
            if task_type == "user_stories":
                result = await self._generate_user_stories(feature, requirements)
            elif task_type == "backlog":
                result = await self._generate_backlog(feature)
            elif task_type == "tech_spec":
                result = await self._generate_tech_spec(feature, requirements)
            elif task_type == "sprint_planning":
                result = await self._sprint_planning(task_input)
            else:
                result = await self._general_dev_task(task_input)
            
            # Store in context for other agents
            self.update_context("dev_artifacts", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _generate_user_stories(self, feature: str, requirements: List[str]) -> Dict[str, Any]:
        """Generate user stories with acceptance criteria"""
        prompt = f"Generate user stories for feature: {feature} with requirements: {requirements}"
        llm_response = await self._call_llm(prompt)
        
        stories = [
            {
                "id": "PROD-101",
                "title": "As a PM, I want AI agent dashboard so I can monitor agent activities",
                "description": "Create a dashboard that shows all active agents and their current tasks",
                "acceptance_criteria": [
                    "Display all 7 agents with status indicators",
                    "Show current task for each agent",
                    "Update in real-time via WebSocket",
                    "Display task history and timeline"
                ],
                "story_points": 8,
                "priority": "High",
                "dependencies": []
            },
            {
                "id": "PROD-102",
                "title": "As a PM, I want to chat with AI copilot so I can get quick insights",
                "description": "Implement chat interface for natural language interaction",
                "acceptance_criteria": [
                    "Support text input with auto-complete",
                    "Display agent responses with formatting",
                    "Maintain conversation history",
                    "Support multi-turn conversations"
                ],
                "story_points": 5,
                "priority": "High",
                "dependencies": ["PROD-101"]
            },
            {
                "id": "PROD-103",
                "title": "As a PM, I want automated sprint summaries so I save time on reporting",
                "description": "Automation agent generates sprint summaries automatically",
                "acceptance_criteria": [
                    "Collect data from Jira API",
                    "Generate narrative summary",
                    "Include key metrics and achievements",
                    "Send via Slack automatically"
                ],
                "story_points": 13,
                "priority": "Medium",
                "dependencies": ["PROD-101"]
            }
        ]
        
        return {
            "feature": feature,
            "stories": stories,
            "total_story_points": sum(s["story_points"] for s in stories),
            "estimated_sprints": 2,
            "synthesis": llm_response
        }
    
    async def _generate_backlog(self, feature: str) -> Dict[str, Any]:
        """Generate product backlog"""
        prompt = f"Create product backlog for: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "epics": [
                {
                    "name": "AI Agent Framework",
                    "description": "Build multi-agent orchestration system",
                    "stories": 8,
                    "story_points": 34
                },
                {
                    "name": "Frontend Dashboard",
                    "description": "Create modern React dashboard with real-time updates",
                    "stories": 12,
                    "story_points": 55
                },
                {
                    "name": "Integrations",
                    "description": "Connect with Jira, Slack, Figma, etc.",
                    "stories": 6,
                    "story_points": 21
                }
            ],
            "prioritization": "RICE framework",
            "backlog_summary": llm_response
        }
    
    async def _generate_tech_spec(self, feature: str, requirements: List[str]) -> Dict[str, Any]:
        """Generate technical specification"""
        prompt = f"Create technical spec for: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "architecture": {
                "frontend": "React + TailwindCSS + Framer Motion",
                "backend": "FastAPI + Python",
                "ai": "LangGraph + Ollama + Nemotron",
                "storage": "SQLite + FAISS",
                "deployment": "Railway/Render"
            },
            "api_endpoints": [
                {
                    "path": "/api/v1/run_task",
                    "method": "POST",
                    "description": "Trigger multi-agent workflow"
                },
                {
                    "path": "/api/v1/projects",
                    "method": "GET",
                    "description": "List all projects"
                },
                {
                    "path": "/ws/agents",
                    "method": "WebSocket",
                    "description": "Real-time agent updates"
                }
            ],
            "data_models": [
                "Project", "AgentTask", "Conversation", "ContextMemory"
            ],
            "security_considerations": [
                "API key encryption",
                "Local LLM for sensitive data",
                "CORS configuration",
                "Rate limiting"
            ],
            "spec_details": llm_response
        }
    
    async def _sprint_planning(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Plan sprint with capacity and velocity"""
        prompt = f"Plan sprint: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "sprint_number": 1,
            "capacity": 40,
            "velocity": 35,
            "selected_stories": ["PROD-101", "PROD-102"],
            "total_points": 13,
            "sprint_goal": "Deliver MVP with basic agent orchestration and dashboard",
            "risks": [
                "Nemotron API integration complexity",
                "WebSocket performance at scale"
            ],
            "plan": llm_response
        }
    
    async def _general_dev_task(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general development tasks"""
        prompt = f"Process development task: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "task": task_input,
            "output": llm_response
        }

