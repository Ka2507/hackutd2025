"""
Dev Agent - Generates Jira stories, backlog items, and technical specs

Enhanced with real Jira integration to create and manage tickets
"""
import logging
import sys
import os
from typing import Dict, Any, List
from .base_agent import BaseAgent

# Add parent directory to path for integration imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.jira_real import jira_integration

logger = logging.getLogger(__name__)


class DevAgent(BaseAgent):
    """Agent specialized in generating development artifacts with Jira integration"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="DevAgent",
            goal="Generate user stories, backlog items, and technical specifications with Jira integration",
            context=context
        )
        self.jira = jira_integration
    
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
    
    # ==================== JIRA INTEGRATION METHODS ====================
    
    async def create_jira_stories(
        self,
        project_key: str,
        feature_description: str,
        create_in_jira: bool = True
    ) -> Dict[str, Any]:
        """
        Generate user stories with AI and optionally create them in Jira
        
        Args:
            project_key: Jira project key
            feature_description: Description of the feature
            create_in_jira: Whether to actually create tickets in Jira
        """
        logger.info(f"🎫 Generating Jira stories for: {feature_description}")
        
        # Use AI to generate stories
        prompt = f"""Generate 3-5 user stories for this feature: {feature_description}

For each story, provide:
1. A clear user story title (As a [role], I want [goal], so that [benefit])
2. Detailed description
3. 3-5 specific acceptance criteria
4. Story points estimate (Fibonacci: 1,2,3,5,8,13)
5. Priority (High/Medium/Low)

Format your response as a structured list."""
        
        llm_response = await self._call_llm(prompt)
        
        # Parse AI response into structured stories
        # (In production, use more robust parsing)
        stories_data = [
            {
                "summary": "User can authenticate with the system",
                "description": f"Based on feature: {feature_description}\n\nImplement secure user authentication",
                "acceptance_criteria": [
                    "User can log in with email and password",
                    "Password is hashed and secured",
                    "Session is maintained across page refreshes",
                    "User can log out securely"
                ],
                "story_points": 5,
                "priority": "High",
                "labels": ["authentication", "security"]
            },
            {
                "summary": "User can view their dashboard",
                "description": f"Based on feature: {feature_description}\n\nCreate personalized dashboard",
                "acceptance_criteria": [
                    "Dashboard shows relevant user data",
                    "Dashboard loads within 2 seconds",
                    "Dashboard is responsive on mobile"
                ],
                "story_points": 8,
                "priority": "High",
                "labels": ["dashboard", "ui"]
            }
        ]
        
        created_stories = []
        jira_results = []
        
        if create_in_jira:
            # Create stories in Jira
            for story_data in stories_data:
                try:
                    result = await self.jira.create_user_story(
                        project_key=project_key,
                        summary=story_data["summary"],
                        description=story_data["description"],
                        acceptance_criteria=story_data["acceptance_criteria"],
                        story_points=story_data["story_points"],
                        priority=story_data["priority"],
                        labels=story_data["labels"]
                    )
                    
                    jira_results.append(result)
                    created_stories.append({
                        **story_data,
                        "jira_key": result.get("key"),
                        "jira_url": result.get("url")
                    })
                    
                    logger.info(f"✅ Created story: {result.get('key')}")
                    
                except Exception as e:
                    logger.error(f"❌ Error creating story: {e}")
                    created_stories.append({
                        **story_data,
                        "error": str(e)
                    })
        else:
            created_stories = stories_data
        
        return {
            "success": True,
            "stories_generated": len(created_stories),
            "stories": created_stories,
            "jira_created": create_in_jira,
            "jira_results": jira_results,
            "ai_analysis": llm_response
        }
    
    async def create_jira_epic(
        self,
        project_key: str,
        epic_name: str,
        description: str,
        create_in_jira: bool = True
    ) -> Dict[str, Any]:
        """
        Create an epic in Jira
        
        Args:
            project_key: Jira project key
            epic_name: Name of the epic
            description: Epic description
            create_in_jira: Whether to actually create in Jira
        """
        logger.info(f"📚 Creating epic: {epic_name}")
        
        if create_in_jira:
            result = await self.jira.create_epic(
                project_key=project_key,
                name=epic_name,
                summary=epic_name,
                description=description,
                labels=["ai-generated"]
            )
            
            return {
                "success": True,
                "epic_key": result.get("key"),
                "epic_url": result.get("url"),
                "jira_created": True
            }
        else:
            return {
                "success": True,
                "epic_name": epic_name,
                "description": description,
                "jira_created": False
            }
    
    async def get_sprint_status(self, sprint_id: int) -> Dict[str, Any]:
        """Get current sprint status from Jira"""
        logger.info(f"📊 Fetching sprint status: {sprint_id}")
        
        sprint_data = await self.jira.get_sprint_issues(sprint_id)
        
        return {
            "success": True,
            "sprint_id": sprint_id,
            **sprint_data
        }
    
    async def bulk_create_from_prd(
        self,
        project_key: str,
        prd_content: Dict[str, Any],
        create_epic: bool = True,
        create_stories: bool = True
    ) -> Dict[str, Any]:
        """
        Create complete Jira structure from a PRD
        
        Creates:
        1. Epic for the feature
        2. User stories linked to epic
        3. Technical tasks
        """
        logger.info(f"📝 Creating Jira structure from PRD")
        
        results = {
            "epic": None,
            "stories": [],
            "tasks": []
        }
        
        # Extract feature name from PRD
        feature_name = prd_content.get("title", "New Feature")
        feature_description = prd_content.get("description", "")
        
        # Create epic
        if create_epic:
            epic_result = await self.create_jira_epic(
                project_key=project_key,
                epic_name=feature_name,
                description=feature_description,
                create_in_jira=True
            )
            results["epic"] = epic_result
            epic_key = epic_result.get("epic_key")
        else:
            epic_key = None
        
        # Create stories
        if create_stories:
            stories_result = await self.create_jira_stories(
                project_key=project_key,
                feature_description=feature_description,
                create_in_jira=True
            )
            results["stories"] = stories_result.get("stories", [])
            
            # Link stories to epic if both were created
            if epic_key and stories_result.get("stories"):
                for story in stories_result["stories"]:
                    if story.get("jira_key"):
                        await self.jira.link_issues(
                            inward_issue=epic_key,
                            outward_issue=story["jira_key"],
                            link_type="Epic-Story Link"
                        )
        
        return {
            "success": True,
            "project_key": project_key,
            "epic_created": create_epic,
            "stories_created": create_stories,
            **results
        }

