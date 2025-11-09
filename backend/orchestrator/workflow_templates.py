"""
Workflow Templates - Pre-built and custom workflow templates
"""
from typing import Dict, Any, List, Optional
from enum import Enum
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import logger


class WorkflowTemplate:
    """Represents a workflow template"""
    
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[str],
        agent_configs: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        self.name = name
        self.description = description
        self.agents = agents
        self.agent_configs = agent_configs or {}
        self.usage_count = 0


# Pre-built workflow templates
WORKFLOW_TEMPLATES = {
    "new_feature_launch": WorkflowTemplate(
        name="New Feature Launch",
        description="Complete feature planning from ideation to launch",
        agents=["strategy", "research", "risk", "dev", "prioritization", "prototype", "gtm", "automation", "regulation"],
        agent_configs={
            "strategy": {"task_type": "idea_generation"},
            "research": {"task_type": "user_research"},
            "dev": {"task_type": "user_stories"},
            "prioritization": {"method": "multi_factor"}
        }
    ),
    "competitive_response": WorkflowTemplate(
        name="Competitive Response",
        description="Rapid response to competitor move",
        agents=["research", "strategy", "dev", "prioritization"],
        agent_configs={
            "research": {"task_type": "competitive_analysis"},
            "strategy": {"task_type": "competitive_analysis"}
        }
    ),
    "compliance_audit": WorkflowTemplate(
        name="Compliance Audit",
        description="Compliance check and fixes",
        agents=["regulation", "risk", "dev"],
        agent_configs={
            "regulation": {"task_type": "compliance_check"}
        }
    ),
    "sprint_planning": WorkflowTemplate(
        name="Sprint Planning",
        description="Plan sprint with prioritization",
        agents=["dev", "prioritization", "automation"],
        agent_configs={
            "dev": {"task_type": "sprint_planning"},
            "prioritization": {"method": "value_effort"}
        }
    ),
    "market_research": WorkflowTemplate(
        name="Market Research",
        description="Deep market and user research",
        agents=["research", "strategy", "risk"],
        agent_configs={
            "research": {"task_type": "user_research"},
            "strategy": {"task_type": "market_sizing"}
        }
    ),
    "adaptive": WorkflowTemplate(
        name="Adaptive Workflow",
        description="AI-powered adaptive workflow that selects agents dynamically",
        agents=["adaptive"],  # Special marker
        agent_configs={}
    )
}


class WorkflowTemplateEngine:
    """Manages workflow templates and recommendations"""
    
    def __init__(self):
        self.templates = WORKFLOW_TEMPLATES
        self.custom_templates = {}
    
    def get_template(self, template_name: str) -> Optional[WorkflowTemplate]:
        """Get template by name"""
        if template_name in self.templates:
            return self.templates[template_name]
        if template_name in self.custom_templates:
            return self.custom_templates[template_name]
        return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates"""
        templates = []
        
        for name, template in self.templates.items():
            templates.append({
                "name": name,
                "display_name": template.name,
                "description": template.description,
                "agents": template.agents,
                "usage_count": template.usage_count,
                "type": "prebuilt"
            })
        
        for name, template in self.custom_templates.items():
            templates.append({
                "name": name,
                "display_name": template.name,
                "description": template.description,
                "agents": template.agents,
                "usage_count": template.usage_count,
                "type": "custom"
            })
        
        return templates
    
    def get_recommended_template(
        self,
        project_context: Dict[str, Any]
    ) -> Optional[WorkflowTemplate]:
        """
        Recommend best template based on project context
        
        Args:
            project_context: Project description, goals, etc.
            
        Returns:
            Recommended template
        """
        context_lower = str(project_context).lower()
        
        # Simple keyword matching - in production, use semantic similarity
        if "compliance" in context_lower or "regulation" in context_lower:
            return self.templates["compliance_audit"]
        elif "competitor" in context_lower or "competitive" in context_lower:
            return self.templates["competitive_response"]
        elif "sprint" in context_lower or "planning" in context_lower:
            return self.templates["sprint_planning"]
        elif "market" in context_lower or "research" in context_lower:
            return self.templates["market_research"]
        elif "feature" in context_lower or "launch" in context_lower:
            return self.templates["new_feature_launch"]
        else:
            return self.templates["adaptive"]  # Default to adaptive
    
    def create_custom_template(
        self,
        name: str,
        description: str,
        agents: List[str],
        agent_configs: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> WorkflowTemplate:
        """Create a custom workflow template"""
        template = WorkflowTemplate(
            name=name,
            description=description,
            agents=agents,
            agent_configs=agent_configs or {}
        )
        
        self.custom_templates[name] = template
        logger.info(f"Created custom template: {name}")
        
        return template
    
    def increment_usage(self, template_name: str):
        """Increment usage count for template"""
        if template_name in self.templates:
            self.templates[template_name].usage_count += 1
        elif template_name in self.custom_templates:
            self.custom_templates[template_name].usage_count += 1


# Global instance
workflow_template_engine = WorkflowTemplateEngine()


