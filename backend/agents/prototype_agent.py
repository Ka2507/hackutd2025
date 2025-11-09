"""
Prototype Agent - Integrates with Figma and creates design mockups
"""
from typing import Dict, Any
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from .base_agent import BaseAgent
from integrations.figma_api import figma_api
from utils.logger import logger


class PrototypeAgent(BaseAgent):
    """Agent specialized in prototyping and design integration"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="PrototypeAgent",
            goal="Create design mockups and integrate with Figma",
            context=context
        )
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute prototype-related tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "wireframe", "mockup", "design_system"
                - feature: Feature to prototype
                - style: Design style preferences
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "wireframe")
        feature = task_input.get("feature", "")
        style = task_input.get("style", "modern")
        
        try:
            if task_type == "wireframe":
                result = await self._create_wireframe(feature)
            elif task_type == "mockup":
                result = await self._create_mockup(feature, style)
            elif task_type == "design_system":
                result = await self._create_design_system()
            else:
                result = await self._general_prototype(task_input)
            
            self.update_context("prototype_assets", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _create_wireframe(self, feature: str) -> Dict[str, Any]:
        """Create wireframes for a feature and optionally create Figma file"""
        prompt = f"""Design comprehensive wireframes for: {feature}

Include:
- Layout structure
- Component hierarchy
- User flow
- Key interactions
- Responsive breakpoints

Format as detailed wireframe specification."""
        llm_response = await self._call_llm(prompt, model="local")
        
        wireframes = [
                {
                    "name": "Dashboard Layout",
                    "components": [
                        "Header with logo and project selector",
                        "Sidebar navigation",
                        "Agent panel grid",
                        "Chat interface",
                        "Timeline visualization"
                    ],
                    "figma_url": "https://figma.com/mockup/dashboard",
                    "notes": "Futuristic but minimal design"
                },
                {
                    "name": "Agent Card",
                    "components": [
                        "Agent name and icon",
                        "Status indicator",
                        "Current task description",
                        "Progress bar",
                        "Action buttons"
                    ],
                    "figma_url": "https://figma.com/mockup/agent-card",
                    "notes": "Use neon cyan accent for active state"
                }
            ]
        
        # Create Figma file if integration is available
        figma_files = []
        if figma_api.connected:
            try:
                # Get or create Figma project
                team_id = self.context.get("figma_team_id", "default")
                projects = await figma_api.get_team_projects(team_id)
                
                if projects:
                    project = projects[0]
                    # Create prototype link for first wireframe
                    if project.get("files"):
                        file_key = project["files"][0]["key"]
                        prototype_link = await figma_api.create_prototype_link(file_key, "0:1")
                        wireframes[0]["figma_prototype_url"] = prototype_link.get("url")
                        figma_files.append({
                            "file_key": file_key,
                            "prototype_url": prototype_link.get("url")
                        })
            except Exception as e:
                logger.warning(f"Failed to create Figma prototype: {e}")
        
        return {
            "feature": feature,
            "wireframes": wireframes,
            "figma_files": figma_files,
            "design_notes": llm_response,
            "integration_status": {
                "figma": "connected" if figma_api.connected else "mock"
            }
        }
    
    async def _create_mockup(self, feature: str, style: str) -> Dict[str, Any]:
        """Create high-fidelity mockups"""
        prompt = f"Create {style} mockup for: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "style": style,
            "mockups": [
                {
                    "screen": "Main Dashboard",
                    "resolution": "1920x1080",
                    "colors": {
                        "base": "#0F1117",
                        "accent_cyan": "#00FFFF",
                        "accent_orange": "#FF7A00",
                        "text": "#FFFFFF"
                    },
                    "typography": {
                        "heading": "Orbitron",
                        "body": "Inter"
                    },
                    "figma_url": "https://figma.com/file/dashboard-mockup",
                    "interactive_prototype": True
                },
                {
                    "screen": "Chat Interface",
                    "resolution": "1920x1080",
                    "key_interactions": [
                        "Message input with auto-complete",
                        "Agent responses with animated appearance",
                        "Task cards expand on click"
                    ],
                    "figma_url": "https://figma.com/file/chat-mockup"
                }
            ],
            "design_details": llm_response,
            "accessibility_notes": [
                "WCAG 2.1 AA compliant",
                "Keyboard navigation supported",
                "High contrast mode available"
            ]
        }
    
    async def _create_design_system(self) -> Dict[str, Any]:
        """Create design system documentation"""
        prompt = "Create comprehensive design system"
        llm_response = await self._call_llm(prompt)
        
        return {
            "colors": {
                "primary": {
                    "charcoal": "#0F1117",
                    "neon_cyan": "#00FFFF",
                    "soft_orange": "#FF7A00"
                },
                "semantic": {
                    "success": "#00FF88",
                    "warning": "#FFB800",
                    "error": "#FF4444",
                    "info": "#00AAFF"
                },
                "neutral": {
                    "gray_100": "#1A1D29",
                    "gray_200": "#2A2E3A",
                    "gray_300": "#3A3E4A"
                }
            },
            "typography": {
                "font_families": {
                    "heading": "Orbitron, sans-serif",
                    "body": "Inter, sans-serif",
                    "mono": "Fira Code, monospace"
                },
                "scales": {
                    "h1": "2.5rem / 40px",
                    "h2": "2rem / 32px",
                    "h3": "1.5rem / 24px",
                    "body": "1rem / 16px",
                    "small": "0.875rem / 14px"
                }
            },
            "spacing": {
                "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64],
                "unit": "px"
            },
            "components": {
                "button": {
                    "variants": ["primary", "secondary", "ghost"],
                    "sizes": ["sm", "md", "lg"],
                    "states": ["default", "hover", "active", "disabled"]
                },
                "card": {
                    "variants": ["default", "agent", "task"],
                    "elevation": [0, 2, 4, 8]
                },
                "input": {
                    "variants": ["text", "textarea", "select"],
                    "states": ["default", "focus", "error"]
                }
            },
            "animations": {
                "durations": {
                    "fast": "150ms",
                    "normal": "300ms",
                    "slow": "500ms"
                },
                "easings": {
                    "ease_in_out": "cubic-bezier(0.4, 0, 0.2, 1)",
                    "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
                }
            },
            "design_system_url": "https://figma.com/file/prodigypm-design-system",
            "documentation": llm_response
        }
    
    async def _general_prototype(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general prototyping tasks"""
        prompt = f"Create prototype for: {task_input}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "task": task_input,
            "prototype_url": "https://figma.com/proto/general",
            "output": llm_response
        }

