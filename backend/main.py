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
from demo_scenarios import get_demo_scenario, list_demo_scenarios

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
    allow_origins=settings.cors_origins,
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
            
            prompt = f"""You are the {agent.name} in a product management AI system.

Your role: {agent.goal}

Recent conversation:
{context_messages}

User's current question/input: {message}

Provide a helpful, detailed response based on your expertise. Be specific and actionable."""
            
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
                    "tokens": last_call.get("tokens", {})
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
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    )

