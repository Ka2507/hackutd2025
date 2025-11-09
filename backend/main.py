"""
ProdigyPM FastAPI Backend
Main application with REST API and WebSocket support
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from utils.config import settings
from utils.logger import logger
from db.context_store import context_store
from orchestrator.task_graph import task_graph, WorkflowType
from orchestrator.memory_manager import memory_manager
from orchestrator.nemotron_bridge import nemotron_bridge
from orchestrator.cost_aware_orchestrator import CostAwareOrchestrator
from orchestrator.workflow_templates import workflow_template_engine
from integrations import jira_api, slack_api, figma_api, reddit_api
from integrations.jira_real import jira_integration
from integrations.figma_real import figma_integration
from integrations.slack_real import slack_integration
from demo_scenarios import get_demo_scenario, list_demo_scenarios
from templates.story_templates import get_template, get_all_templates, list_template_names, format_story_for_pnc, generate_pnc_demo_stories
from templates.story_exporter import exporter

# Initialize cost-aware orchestrator
cost_orchestrator = CostAwareOrchestrator(total_budget=settings.total_budget)


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Agentic AI platform for Product Managers"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)


manager = ConnectionManager()


# Pydantic models for API requests
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class TaskRunRequest(BaseModel):
    workflow_type: str
    input_data: Dict[str, Any]
    project_id: Optional[int] = None
    use_nemotron: bool = True


class ConversationMessage(BaseModel):
    project_id: int
    message: str
    metadata: Optional[Dict[str, Any]] = None


class AgentTaskRequest(BaseModel):
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    project_id: Optional[int] = None


class RiskAssessmentRequest(BaseModel):
    workflow_state: Dict[str, Any]
    project_id: Optional[int] = None
    risk_factors: Optional[List[str]] = None


class PrioritizationRequest(BaseModel):
    features: List[Dict[str, Any]]
    context: Dict[str, Any]
    method: str = "multi_factor"


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(task_graph.agents),
        "integrations": {
            "jira": jira_api.health_check(),
            "slack": slack_api.health_check(),
            "figma": figma_api.health_check(),
            "reddit": reddit_api.health_check()
        },
        "memory_stats": memory_manager.get_stats(),
        "nemotron_usage": nemotron_bridge.get_usage_stats()
    }


# Project Management

@app.post("/api/v1/projects")
async def create_project(project: ProjectCreate):
    """Create a new project"""
    try:
        project_id = context_store.create_project(project.name, project.description)
        
        # Broadcast project creation
        await manager.broadcast({
            "type": "project_created",
            "data": {
                "project_id": project_id,
                "name": project.name
            }
        })
        
        return {
            "success": True,
            "project_id": project_id,
            "message": "Project created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/projects")
async def list_projects():
    """List all projects"""
    try:
        projects = context_store.list_projects()
        return {
            "success": True,
            "projects": projects,
            "count": len(projects)
        }
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: int):
    """Get project details"""
    try:
        project = context_store.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get related data
        conversations = context_store.get_conversation_history(project_id)
        tasks = context_store.get_agent_tasks(project_id)
        
        return {
            "success": True,
            "project": project,
            "conversations": conversations,
            "tasks": tasks
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Agent and Workflow Management

@app.post("/api/v1/run_task")
async def run_task(request: TaskRunRequest):
    """
    Trigger multi-agent workflow
    This is the main endpoint for executing AI agent workflows
    """
    try:
        logger.info(f"Starting task: {request.workflow_type}")
        
        # Broadcast task start
        await manager.broadcast({
            "type": "task_started",
            "data": {
                "workflow_type": request.workflow_type,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        # Execute workflow
        result = await task_graph.execute_workflow(
            workflow_type=request.workflow_type,
            input_data=request.input_data,
            project_id=request.project_id,
            use_nemotron=request.use_nemotron
        )
        
        # Store in context if project specified
        if request.project_id:
            context_store.add_conversation(
                project_id=request.project_id,
                role="system",
                content=f"Executed workflow: {request.workflow_type}",
                metadata={"workflow_result": result}
            )
        
        # Broadcast task completion
        await manager.broadcast({
            "type": "task_completed",
            "data": {
                "workflow_type": request.workflow_type,
                "workflow_id": result.get("workflow_id"),
                "status": result.get("status"),
                "timestamp": datetime.now().isoformat()
            }
        })
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error running task: {e}")
        
        # Broadcast task failure
        await manager.broadcast({
            "type": "task_failed",
            "data": {
                "workflow_type": request.workflow_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        })
        
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/{agent_name}/execute")
async def execute_single_agent(agent_name: str, request: AgentTaskRequest):
    """Execute a single agent task"""
    try:
        if agent_name not in task_graph.agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        agent = task_graph.agents[agent_name]
        
        # Broadcast agent start
        await manager.broadcast({
            "type": "agent_started",
            "data": {
                "agent": agent_name,
                "task_type": request.task_type,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        # Check if this is a chat message
        if request.task_type == "chat":
            # Handle interactive chat with agent
            message = request.input_data.get("message", "")
            conversation_history = request.input_data.get("conversation_history", [])
            
            # Build context-aware prompt
            context_messages = "\n".join([
                f"{msg['role'].title()}: {msg['content']}" 
                for msg in conversation_history[-5:]  # Last 5 messages for context
            ])
            
            # Get agent-specific expertise and related agents
            agent_expertise = {
                "strategy": {
                    "focus": "Market analysis, competitive intelligence, business strategy, market sizing, positioning",
                    "redirect_to": {
                        "user research": "Research Agent",
                        "technical specs": "Dev Agent",
                        "design": "Prototype Agent",
                        "compliance": "Regulation Agent",
                        "launch planning": "GTM Agent"
                    }
                },
                "research": {
                    "focus": "User insights, trend detection, competitive research, market validation, user feedback analysis",
                    "redirect_to": {
                        "strategy": "Strategy Agent",
                        "development": "Dev Agent",
                        "compliance": "Regulation Agent"
                    }
                },
                "dev": {
                    "focus": "User stories, technical specifications, backlog creation, sprint planning, acceptance criteria",
                    "redirect_to": {
                        "design": "Prototype Agent",
                        "strategy": "Strategy Agent",
                        "compliance": "Regulation Agent"
                    }
                },
                "development": {
                    "focus": "User stories, technical specifications, backlog creation, sprint planning, acceptance criteria",
                    "redirect_to": {
                        "design": "Prototype Agent",
                        "strategy": "Strategy Agent"
                    }
                },
                "prototype": {
                    "focus": "Design mockups, wireframes, UI/UX specifications, Figma integration, component libraries",
                    "redirect_to": {
                        "development": "Dev Agent",
                        "research": "Research Agent",
                        "launch": "GTM Agent"
                    }
                },
                "gtm": {
                    "focus": "Go-to-market strategy, launch planning, pricing, marketing messaging, channel strategy",
                    "redirect_to": {
                        "strategy": "Strategy Agent",
                        "research": "Research Agent",
                        "compliance": "Regulation Agent"
                    }
                },
                "go-to-market": {
                    "focus": "Go-to-market strategy, launch planning, pricing, marketing messaging, channel strategy",
                    "redirect_to": {
                        "strategy": "Strategy Agent"
                    }
                },
                "automation": {
                    "focus": "Workflow automation, sprint reports, standup summaries, process optimization",
                    "redirect_to": {
                        "development": "Dev Agent",
                        "strategy": "Strategy Agent"
                    }
                },
                "regulation": {
                    "focus": "Compliance requirements, regulatory review, risk assessment, privacy (GDPR, SOC2, PCI-DSS)",
                    "redirect_to": {
                        "risk": "Risk Assessment Agent",
                        "development": "Dev Agent"
                    }
                },
                "prioritization": {
                    "focus": "Feature prioritization, RICE framework, value/effort analysis, roadmap planning",
                    "redirect_to": {
                        "strategy": "Strategy Agent",
                        "development": "Dev Agent"
                    }
                },
                "risk_assessment": {
                    "focus": "Risk analysis, bottleneck prediction, mitigation strategies, technical and business risks",
                    "redirect_to": {
                        "compliance": "Regulation Agent",
                        "strategy": "Strategy Agent"
                    }
                }
            }
            
            expertise = agent_expertise.get(agent_name, {
                "focus": agent.goal,
                "redirect_to": {}
            })
            
            redirects_text = "\n".join([
                f"- For {topic} questions → suggest they ask the {target_agent}"
                for topic, target_agent in expertise["redirect_to"].items()
            ])
            
            prompt = f"""You are the {agent.name}, a specialized AI agent in a product management system.

YOUR EXPERTISE: {expertise["focus"]}

YOUR ROLE: {agent.goal}

IMPORTANT INSTRUCTIONS:
1. ONLY answer questions directly related to your expertise areas
2. Provide detailed, specific, actionable insights in your domain
3. If the user asks about topics OUTSIDE your expertise, politely redirect them:
{redirects_text if redirects_text else "   - Direct them to the appropriate specialized agent"}
4. Be professional, helpful, and specific
5. Use examples and frameworks relevant to your domain

RECENT CONVERSATION:
{context_messages if context_messages else "This is the start of the conversation."}

USER'S QUESTION: {message}

RESPONSE (answer if in your expertise, otherwise redirect):"""
            
            # Special handling for Prototype Agent design requests
            mockup_data = None
            if agent_name == "prototype" and any(keyword in message.lower() for keyword in ["mockup", "design", "wireframe", "ui", "interface", "screen"]):
                logger.info(f"🎨 Detected design request for Prototype Agent")
                try:
                    mockup_data = await agent.generate_mockup_from_chat(message)
                    logger.info(f"✅ Generated mockup with {len(mockup_data.get('screens', []))} screens")
                except Exception as e:
                    logger.error(f"❌ Error generating mockup: {e}")
            
            # Call NVIDIA API through the agent
            response_text = await agent._call_llm(prompt, use_nvidia=True)
            
            # Get the last API call stats from nemotron_bridge
            stats = nemotron_bridge.get_usage_stats()
            last_call = stats['call_history'][-1] if stats['call_history'] else {}
            
            result = {
                "agent": agent.name,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "result": {
                    "response": response_text,
                    "model": last_call.get("model", "unknown"),
                    "cost": last_call.get("cost", 0),
                    "tokens": last_call.get("tokens", {}),
                    "mockup": mockup_data  # Include mockup if generated
                }
            }
        else:
            # Execute normal agent task
            result = await agent.execute(request.input_data)
        
        # Store task in database if project specified
        if request.project_id:
            task_id = context_store.create_agent_task(
                project_id=request.project_id,
                agent_name=agent_name,
                task_type=request.task_type,
                input_data=request.input_data
            )
            context_store.update_agent_task(task_id, "completed", result)
        
        # Broadcast agent completion
        await manager.broadcast({
            "type": "agent_completed",
            "data": {
                "agent": agent_name,
                "task_type": request.task_type,
                "status": result.get("status"),
                "timestamp": datetime.now().isoformat()
            }
        })
        
        return {
            "success": True,
            "agent": agent_name,
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing agent {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agents")
async def get_agents_status():
    """Get status of all agents"""
    try:
        status = task_graph.get_agent_status()
        return {
            "success": True,
            "agents": status,
            "count": len(status)
        }
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows")
async def list_workflows():
    """List available workflow types"""
    return {
        "success": True,
        "workflows": [
            {
                "type": WorkflowType.FULL_FEATURE_PLANNING.value,
                "description": "Complete feature planning workflow (all agents)",
                "agents": ["strategy", "research", "dev", "prototype", "gtm", "automation", "regulation"]
            },
            {
                "type": WorkflowType.RESEARCH_AND_STRATEGY.value,
                "description": "Research and strategic analysis",
                "agents": ["research", "strategy"]
            },
            {
                "type": WorkflowType.DEV_PLANNING.value,
                "description": "Development planning and prototyping",
                "agents": ["dev", "prototype"]
            },
            {
                "type": WorkflowType.LAUNCH_PLANNING.value,
                "description": "Go-to-market and launch planning",
                "agents": ["gtm", "automation"]
            },
            {
                "type": WorkflowType.COMPLIANCE_CHECK.value,
                "description": "Compliance and regulatory review",
                "agents": ["regulation"]
            }
        ]
    }


@app.get("/api/v1/workflows/history")
async def get_workflow_history(limit: int = 10):
    """Get recent workflow execution history"""
    try:
        history = task_graph.get_workflow_history(limit)
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting workflow history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/generate_prd")
async def generate_prd(workflow_id: str = None, project_id: int = None):
    """
    Generate PRD from completed workflow results.
    
    This endpoint can be called after running a full_feature_planning
    workflow to generate a comprehensive PRD document.
    """
    try:
        # For demo, we'll generate from the last workflow
        # In production, fetch specific workflow by ID
        
        # Get latest workflow from history
        history = task_graph.get_workflow_history(limit=1)
        if not history:
            raise HTTPException(
                status_code=404,
                detail="No workflow found to generate PRD from"
            )
        
        # Execute PRD generator with mock workflow results
        prd_result = await task_graph.prd_generator.execute({
            "workflow_results": {
                "steps": [],
                "workflow": "full_feature_planning"
            },
            "product_name": "Sample Product",
            "version": "1.0"
        })
        
        return {
            "success": True,
            "prd": prd_result.get("result", {}),
            "markdown": prd_result.get("result", {}).get("markdown", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Conversation Management

@app.post("/api/v1/conversations")
async def add_conversation(message: ConversationMessage):
    """Add a conversation message"""
    try:
        msg_id = context_store.add_conversation(
            project_id=message.project_id,
            role="user",
            content=message.message,
            metadata=message.metadata
        )
        
        # Broadcast new message
        await manager.broadcast({
            "type": "new_message",
            "data": {
                "project_id": message.project_id,
                "message": message.message,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        return {
            "success": True,
            "message_id": msg_id
        }
    except Exception as e:
        logger.error(f"Error adding conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/conversations/{project_id}")
async def get_conversations(project_id: int, limit: int = 50):
    """Get conversation history for a project"""
    try:
        conversations = context_store.get_conversation_history(project_id, limit)
        return {
            "success": True,
            "conversations": conversations,
            "count": len(conversations)
        }
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Integration Endpoints

@app.get("/api/v1/integrations/jira/sprint/{sprint_id}")
async def get_jira_sprint(sprint_id: str):
    """Get Jira sprint data"""
    try:
        data = await jira_api.get_sprint_data(sprint_id)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting Jira sprint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/integrations/reddit/search")
async def search_reddit(subreddit: str, query: str, limit: int = 10):
    """Search Reddit"""
    try:
        results = await reddit_api.search_subreddit(subreddit, query, limit=limit)
        return {"success": True, "results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Error searching Reddit: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/integrations/figma/file/{file_key}")
async def get_figma_file(file_key: str):
    """Get Figma file"""
    try:
        data = await figma_api.get_file(file_key)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error getting Figma file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== COMPREHENSIVE JIRA INTEGRATION ENDPOINTS ====================

class JiraStoryRequest(BaseModel):
    project_key: str
    feature_description: str
    create_in_jira: bool = True


class JiraEpicRequest(BaseModel):
    project_key: str
    epic_name: str
    description: str
    create_in_jira: bool = True


class JiraBulkCreateRequest(BaseModel):
    project_key: str
    prd_content: Dict[str, Any]
    create_epic: bool = True
    create_stories: bool = True


@app.post("/api/v1/jira/create_stories")
async def create_jira_stories_api(request: JiraStoryRequest):
    """Generate and create user stories in Jira using AI"""
    try:
        dev_agent = task_graph.agents.get("dev")
        if not dev_agent:
            raise HTTPException(status_code=404, detail="Dev agent not found")
        
        result = await dev_agent.create_jira_stories(
            project_key=request.project_key,
            feature_description=request.feature_description,
            create_in_jira=request.create_in_jira
        )
        
        return {
            "success": True,
            **result
        }
        
    except Exception as e:
        logger.error(f"Error creating Jira stories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jira/create_epic")
async def create_jira_epic_api(request: JiraEpicRequest):
    """Create an epic in Jira"""
    try:
        dev_agent = task_graph.agents.get("dev")
        if not dev_agent:
            raise HTTPException(status_code=404, detail="Dev agent not found")
        
        result = await dev_agent.create_jira_epic(
            project_key=request.project_key,
            epic_name=request.epic_name,
            description=request.description,
            create_in_jira=request.create_in_jira
        )
        
        return {
            "success": True,
            **result
        }
        
    except Exception as e:
        logger.error(f"Error creating Jira epic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jira/bulk_create_from_prd")
async def bulk_create_from_prd_api(request: JiraBulkCreateRequest):
    """Create complete Jira structure (epic + stories) from a PRD"""
    try:
        dev_agent = task_graph.agents.get("dev")
        if not dev_agent:
            raise HTTPException(status_code=404, detail="Dev agent not found")
        
        result = await dev_agent.bulk_create_from_prd(
            project_key=request.project_key,
            prd_content=request.prd_content,
            create_epic=request.create_epic,
            create_stories=request.create_stories
        )
        
        return {
            "success": True,
            **result
        }
        
    except Exception as e:
        logger.error(f"Error creating from PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/jira/sprint/{sprint_id}/status")
async def get_sprint_status_api(sprint_id: int):
    """Get detailed sprint status"""
    try:
        sprint_data = await jira_integration.get_sprint_issues(sprint_id)
        return {
            "success": True,
            **sprint_data
        }
    except Exception as e:
        logger.error(f"Error getting sprint status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/jira/backlog/{project_key}")
async def get_backlog_api(project_key: str, max_results: int = 50):
    """Get backlog for a project"""
    try:
        backlog = await jira_integration.get_backlog(project_key, max_results)
        return {
            "success": True,
            "backlog": backlog,
            "count": len(backlog)
        }
    except Exception as e:
        logger.error(f"Error getting backlog: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/jira/epic/{epic_key}/stories")
async def get_epic_stories_api(epic_key: str):
    """Get all stories in an epic"""
    try:
        stories = await jira_integration.get_epic_stories(epic_key)
        return {
            "success": True,
            "epic_key": epic_key,
            "stories": stories,
            "count": len(stories)
        }
    except Exception as e:
        logger.error(f"Error getting epic stories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jira/issue/{issue_key}/comment")
async def add_jira_comment_api(issue_key: str, comment: str):
    """Add a comment to a Jira issue"""
    try:
        result = await jira_integration.add_comment(issue_key, comment)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Error adding comment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jira/issue/{issue_key}/transition")
async def transition_issue_api(issue_key: str, transition_name: str):
    """Transition a Jira issue to new status"""
    try:
        result = await jira_integration.transition_issue(issue_key, transition_name)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Error transitioning issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/jira/health")
async def jira_health_check():
    """Check Jira integration health"""
    try:
        health = jira_integration.health_check()
        return {
            "success": True,
            **health
        }
    except Exception as e:
        logger.error(f"Error checking Jira health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== STORY TEMPLATES & EXPORT (PNC Workshop Compatible) ====================

@app.get("/api/v1/templates/list")
async def list_story_templates():
    """List all available story templates (PNC workshop format)"""
    try:
        template_names = list_template_names()
        all_templates = get_all_templates()
        
        templates = []
        for name in template_names:
            template = all_templates[name]
            templates.append({
                "name": name,
                "title": template.get("title", ""),
                "priority": template.get("priority", ""),
                "estimate": template.get("estimate", ""),
                "tags": template.get("tags", []),
                "epic": template.get("epic", "")
            })
        
        return {
            "success": True,
            "templates": templates,
            "count": len(templates),
            "pnc_compatible": True
        }
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/templates/{template_name}")
async def get_story_template(template_name: str):
    """Get a specific story template"""
    try:
        template = get_template(template_name)
        return {
            "success": True,
            "template": template,
            "pnc_format": True
        }
    except Exception as e:
        logger.error(f"Error getting template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/demo/pnc_stories")
async def get_pnc_demo_stories():
    """Get demo stories in PNC workshop format - shows our AI advantage"""
    try:
        stories = generate_pnc_demo_stories()
        return {
            "success": True,
            "stories": stories,
            "count": len(stories),
            "generated_by": "ProdigyPM 9-Agent System",
            "advantage": "Multi-agent review vs single LLM generation",
            "pnc_compatible": True
        }
    except Exception as e:
        logger.error(f"Error generating PNC demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class ExportRequest(BaseModel):
    stories: List[Dict[str, Any]]
    format: str  # csv, json, markdown, jira_csv
    title: Optional[str] = "User Stories"


@app.post("/api/v1/export/stories")
async def export_stories(request: ExportRequest):
    """Export stories in multiple formats (CSV, JSON, Markdown)"""
    try:
        logger.info(f"📤 Exporting {len(request.stories)} stories to {request.format}")
        
        if request.format == "csv":
            content = exporter.to_csv(request.stories)
            media_type = "text/csv"
            filename = f"user_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        elif request.format == "markdown" or request.format == "md":
            content = exporter.to_markdown(request.stories, request.title)
            media_type = "text/markdown"
            filename = f"user_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
        elif request.format == "jira_csv":
            content = exporter.to_jira_import_csv(request.stories)
            media_type = "text/csv"
            filename = f"jira_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        elif request.format == "json":
            content = exporter.to_json(request.stories, pretty=True)
            media_type = "application/json"
            filename = f"user_stories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.format}")
        
        return {
            "success": True,
            "content": content,
            "media_type": media_type,
            "filename": filename,
            "pnc_workshop_compatible": request.format in ["csv", "markdown", "json"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting stories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== FIGMA INTEGRATION ENDPOINTS ====================

@app.get("/api/v1/figma/file/{file_key}")
async def get_figma_file_api(file_key: str):
    """Get Figma file data"""
    try:
        data = await figma_integration.get_file(file_key)
        return {
            "success": True,
            "file": data
        }
    except Exception as e:
        logger.error(f"Error getting Figma file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/figma/file/{file_key}/comment")
async def post_figma_comment_api(file_key: str, message: str):
    """Post comment to Figma file"""
    try:
        result = await figma_integration.create_comment(file_key, message)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Error posting Figma comment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/figma/health")
async def figma_health_check():
    """Check Figma integration health"""
    try:
        health = figma_integration.health_check()
        return {
            "success": True,
            **health
        }
    except Exception as e:
        logger.error(f"Error checking Figma health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SLACK INTEGRATION ENDPOINTS ====================

class SlackMessageRequest(BaseModel):
    channel: str
    message: str


@app.post("/api/v1/slack/send_message")
async def send_slack_message_api(request: SlackMessageRequest):
    """Send a message to Slack"""
    try:
        result = await slack_integration.send_message(request.channel, request.message)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Error sending Slack message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/slack/send_sprint_report")
async def send_sprint_report_slack_api(channel: str, sprint_data: Dict[str, Any]):
    """Send sprint report to Slack"""
    try:
        result = await slack_integration.send_sprint_report(channel, sprint_data)
        return {
            "success": True,
            **result
        }
    except Exception as e:
        logger.error(f"Error sending sprint report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/slack/health")
async def slack_health_check():
    """Check Slack integration health"""
    try:
        health = slack_integration.health_check()
        return {
            "success": True,
            **health
        }
    except Exception as e:
        logger.error(f"Error checking Slack health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates

@app.websocket("/ws/agents")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent updates
    Clients connect here to receive live updates about agent execution
    """
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_json({
            "type": "connected",
            "data": {
                "message": "Connected to ProdigyPM agent updates",
                "timestamp": datetime.now().isoformat(),
                "agents": task_graph.get_agent_status()
            }
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")
            
            # Echo back for now (can add command handling later)
            await websocket.send_json({
                "type": "echo",
                "data": {"message": data}
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# Advanced Features Endpoints

@app.post("/api/v1/risk/assess")
async def assess_risk(request: RiskAssessmentRequest):
    """Assess project risks"""
    try:
        risk_agent = task_graph.agents.get("risk_assessment")
        if not risk_agent:
            raise HTTPException(status_code=404, detail="Risk assessment agent not found")
        
        result = await risk_agent.execute({
            "workflow_state": request.workflow_state,
            "project_id": request.project_id,
            "risk_factors": request.risk_factors or []
        })
        
        return {
            "success": True,
            "risk_assessment": result
        }
    except Exception as e:
        logger.error(f"Error assessing risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/prioritize")
async def prioritize_features(request: PrioritizationRequest):
    """Prioritize features using multi-factor analysis"""
    try:
        prioritization_agent = task_graph.agents.get("prioritization")
        if not prioritization_agent:
            raise HTTPException(status_code=404, detail="Prioritization agent not found")
        
        result = await prioritization_agent.execute({
            "features": request.features,
            "context": request.context,
            "method": request.method
        })
        
        return {
            "success": True,
            "prioritization": result
        }
    except Exception as e:
        logger.error(f"Error prioritizing features: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/budget/status")
async def get_budget_status():
    """Get current budget status"""
    try:
        budget_status = cost_orchestrator.get_budget_status()
        return {
            "success": True,
            "budget": budget_status
        }
    except Exception as e:
        logger.error(f"Error getting budget status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class BudgetUpdateRequest(BaseModel):
    total_budget: float


@app.put("/api/v1/budget/update")
async def update_budget(request: BudgetUpdateRequest):
    """Update total budget"""
    try:
        cost_orchestrator.total_budget = request.total_budget
        return {
            "success": True,
            "message": f"Budget updated to ${request.total_budget}",
            "budget": cost_orchestrator.get_budget_status()
        }
    except Exception as e:
        logger.error(f"Error updating budget: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows/templates")
async def list_workflow_templates():
    """List available workflow templates"""
    try:
        templates = workflow_template_engine.list_templates()
        return {
            "success": True,
            "templates": templates
        }
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows/templates/recommend")
async def recommend_template(project_description: str):
    """Get recommended template based on project description"""
    try:
        template = workflow_template_engine.get_recommended_template({"description": project_description})
        if not template:
            return {
                "success": True,
                "template": None,
                "message": "No specific template recommended, using adaptive workflow"
            }
        
        return {
            "success": True,
            "template": {
                "name": template.name,
                "description": template.description,
                "agents": template.agents
            }
        }
    except Exception as e:
        logger.error(f"Error recommending template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/generate_prd")
async def generate_prd(workflow_id: Optional[str] = None, project_id: Optional[int] = None):
    """Generate a Product Requirements Document"""
    try:
        # Get workflow history if workflow_id provided
        workflow_data = {}
        steps = []
        
        if workflow_id:
            history = task_graph.get_workflow_history(limit=20)
            for wf in history:
                if wf.get("workflow_id") == workflow_id:
                    workflow_data = wf
                    steps = workflow_data.get("results", {}).get("steps", [])
                    break
        
        # Generate PRD structure
        prd = {
            "title": "Product Requirements Document",
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "workflow_id": workflow_id,
            "project_id": project_id,
            "sections": {
                "overview": {
                    "title": "Product Overview",
                    "content": steps[0].get("output", {}).get("data", {}) if len(steps) > 0 else {"note": "Run a workflow to populate this section"}
                },
                "market_analysis": {
                    "title": "Market Analysis",
                    "content": steps[0].get("output", {}).get("data", {}) if len(steps) > 0 else {"note": "Market analysis pending"}
                },
                "user_research": {
                    "title": "User Research",
                    "content": steps[1].get("output", {}).get("data", {}) if len(steps) > 1 else {"note": "User research pending"}
                },
                "risk_assessment": {
                    "title": "Risk Assessment",
                    "content": steps[2].get("output", {}).get("data", {}) if len(steps) > 2 else {"note": "Risk assessment pending"}
                },
                "technical_requirements": {
                    "title": "Technical Requirements",
                    "content": steps[3].get("output", {}).get("data", {}) if len(steps) > 3 else {"note": "Technical requirements pending"}
                },
                "prioritization": {
                    "title": "Feature Prioritization",
                    "content": steps[4].get("output", {}).get("data", {}) if len(steps) > 4 else {"note": "Prioritization pending"}
                },
                "design_specs": {
                    "title": "Design Specifications",
                    "content": steps[5].get("output", {}).get("data", {}) if len(steps) > 5 else {"note": "Design specs pending"}
                },
                "go_to_market": {
                    "title": "Go-to-Market Strategy",
                    "content": steps[6].get("output", {}).get("data", {}) if len(steps) > 6 else {"note": "GTM strategy pending"}
                },
                "automation": {
                    "title": "Automation & Workflows",
                    "content": steps[7].get("output", {}).get("data", {}) if len(steps) > 7 else {"note": "Automation pending"}
                },
                "compliance": {
                    "title": "Compliance & Security",
                    "content": steps[8].get("output", {}).get("data", {}) if len(steps) > 8 else {"note": "Compliance review pending"}
                }
            },
            "generated_by": "ProdigyPM Multi-Agent System",
            "agents_used": list(task_graph.agents.keys()),
            "workflow_completed": len(steps) > 0
        }
        
        return {
            "success": True,
            "prd": prd
        }
    except Exception as e:
        logger.error(f"Error generating PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class QuickPRDRequest(BaseModel):
    product_idea: str
    target_market: Optional[str] = None
    key_features: Optional[List[str]] = None


@app.post("/api/v1/generate_quick_prd")
async def generate_quick_prd(request: QuickPRDRequest):
    """Generate a quick PRD from a single prompt - fast brainstorming mode"""
    try:
        logger.info(f"⚡ Generating Quick PRD for: {request.product_idea[:100]}")
        
        # Use Strategy Agent for fast PRD generation
        strategy_agent = task_graph.agents.get("strategy")
        if not strategy_agent:
            raise HTTPException(status_code=404, detail="Strategy agent not found")
        
        # Build comprehensive prompt for quick PRD
        prompt = f"""Generate a comprehensive Product Requirements Document (PRD) for this product idea:

PRODUCT IDEA: {request.product_idea}
{f"TARGET MARKET: {request.target_market}" if request.target_market else ""}
{f"KEY FEATURES: {', '.join(request.key_features)}" if request.key_features else ""}

Create a complete PRD with these sections:

## 1. Executive Summary
Brief overview of the product (2-3 paragraphs)

## 2. Problem Statement
What problem does this solve? Who has this problem?

## 3. Goals & Success Metrics
What are we trying to achieve? How will we measure success?

## 4. Target Users
Who will use this? User personas and segments.

## 5. Key Features
List of main features with brief descriptions

## 6. User Stories
3-5 key user stories with acceptance criteria

## 7. Technical Requirements
High-level technical approach and architecture

## 8. Design Considerations
UI/UX approach and design principles

## 9. Go-to-Market Strategy
Launch approach and marketing plan

## 10. Timeline & Milestones
Rough timeline with key milestones

## 11. Risks & Mitigation
Potential risks and how to address them

Be specific, actionable, and detailed. Format with markdown."""
        
        # Call Strategy Agent (uses powerful model)
        response = await strategy_agent._call_llm(prompt, use_nvidia=True, use_cache=False)
        
        # Get cost info
        stats = nemotron_bridge.get_usage_stats()
        last_call = stats['call_history'][-1] if stats['call_history'] else {}
        
        # Parse response into sections
        prd = {
            "title": f"PRD: {request.product_idea[:100]}",
            "type": "quick",
            "generated_at": datetime.now().isoformat(),
            "product_idea": request.product_idea,
            "content": response,
            "model_used": last_call.get("model", "unknown"),
            "generation_cost": last_call.get("cost", 0),
            "sections": {
                "executive_summary": {"content": "See full content"},
                "problem_statement": {"content": "See full content"},
                "goals": {"content": "See full content"},
                "target_users": {"content": "See full content"},
                "key_features": {"content": "See full content"},
                "user_stories": {"content": "See full content"},
                "technical_requirements": {"content": "See full content"},
                "design_considerations": {"content": "See full content"},
                "go_to_market": {"content": "See full content"},
                "timeline": {"content": "See full content"},
                "risks": {"content": "See full content"}
            },
            "metadata": {
                "generation_mode": "quick",
                "agents_used": ["Strategy Agent"],
                "total_agents": 1,
                "time_saved": "vs 9-agent detailed PRD"
            }
        }
        
        logger.info(f"✅ Quick PRD generated | Cost: ${last_call.get('cost', 0):.4f}")
        
        return {
            "success": True,
            "prd": prd
        }
        
    except Exception as e:
        logger.error(f"Error generating quick PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/demo/scenarios")
async def list_demos():
    """List all available demo scenarios"""
    try:
        scenarios = list_demo_scenarios()
        return {
            "success": True,
            "scenarios": scenarios
        }
    except Exception as e:
        logger.error(f"Error listing demo scenarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/demo/run")
async def run_demo_scenario(request: Dict[str, Any]):
    """Run a pre-configured demo scenario"""
    try:
        scenario_key = request.get("scenario_key")
        if not scenario_key:
            raise HTTPException(status_code=400, detail="scenario_key is required")
        
        scenario = get_demo_scenario(scenario_key)
        if not scenario:
            raise HTTPException(status_code=404, detail=f"Scenario '{scenario_key}' not found")
        
        # Execute the workflow with demo data
        result = await task_graph.execute_workflow(
            workflow_type=scenario["workflow_type"],
            input_data=scenario["input_data"],
            project_id=None,
            use_nemotron=True
        )
        
        # Broadcast via WebSocket
        await manager.broadcast({
            "type": "demo_completed",
            "scenario": scenario["name"],
            "data": result
        })
        
        return {
            "success": True,
            "scenario": scenario["name"],
            "result": result,
            "expected_outputs": scenario.get("expected_outputs", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running demo scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Startup and shutdown events

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Agents initialized: {list(task_graph.agents.keys())}")
    logger.info(f"Memory manager: {memory_manager.get_stats()}")
    logger.info(f"Nemotron bridge: {nemotron_bridge.get_usage_stats()}")
    
    # Initialize database
    logger.info("Database initialized")
    
    # Create default project if none exist
    projects = context_store.list_projects()
    if not projects:
        default_id = context_store.create_project(
            "Demo Project",
            "Default demonstration project"
        )
        logger.info(f"Created default project: {default_id}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(f"Shutting down {settings.app_name}")
    
    # Save memory to disk
    try:
        memory_manager.save_to_disk()
        logger.info("Memory saved to disk")
    except Exception as e:
        logger.error(f"Error saving memory: {e}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.get_port(),
        reload=settings.debug,
        log_level="info"
    )

