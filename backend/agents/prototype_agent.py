"""
Prototype Agent - Integrates with Figma and creates design mockups

Enhanced to generate visual mockups and wireframes
"""
import logging
import sys
import os
from typing import Dict, Any
from .base_agent import BaseAgent

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.figma_real import figma_integration

logger = logging.getLogger(__name__)


class PrototypeAgent(BaseAgent):
    """Agent specialized in prototyping and design integration"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="PrototypeAgent",
            goal="Create design mockups and integrate with Figma",
            context=context
        )
        self.figma = figma_integration
    
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
        """Create wireframes for a feature"""
        prompt = f"Design wireframe for: {feature}"
        llm_response = await self._call_llm(prompt)
        
        return {
            "feature": feature,
            "wireframes": [
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
            ],
            "design_notes": llm_response
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
    
    async def generate_mockup_from_chat(self, feature_description: str) -> Dict[str, Any]:
        """
        Generate visual mockup when user asks in chat
        
        Args:
            feature_description: Description of what to design
            
        Returns:
            Mockup data with visual elements
        """
        logger.info(f"🎨 Generating mockup for: {feature_description}")
        
        # Use AI to generate design concept
        prompt = f"""You are a UX/UI designer creating a mockup for: {feature_description}

Provide:
1. Screen layout description
2. Key UI components needed
3. Color scheme recommendations
4. User interaction flow
5. Design patterns to use

Be specific and actionable."""
        
        design_concept = await self._call_llm(prompt)
        
        # Generate mockup structure
        mockup = {
            "title": f"Mockup: {feature_description[:100]}",
            "screens": [
                {
                    "name": "Main Screen",
                    "layout": "Modern dashboard layout with sidebar navigation",
                    "components": [
                        {"type": "header", "content": "Navigation bar with logo"},
                        {"type": "sidebar", "content": "Main navigation menu"},
                        {"type": "content", "content": "Primary content area"},
                        {"type": "footer", "content": "Status and actions"}
                    ],
                    "wireframe_svg": self._generate_wireframe_svg(feature_description),
                    "notes": "Clean, modern interface following Material Design principles"
                }
            ],
            "design_concept": design_concept,
            "color_palette": {
                "primary": "#00FFFF",
                "secondary": "#FF7A00",
                "background": "#0F1117",
                "surface": "#1A1D29",
                "text": "#FFFFFF"
            },
            "typography": {
                "heading": "Orbitron",
                "body": "Inter"
            },
            "figma_integration": {
                "available": self.figma.connected,
                "status": "Can export to Figma" if self.figma.connected else "Mock mode - designs are conceptual"
            }
        }
        
        return mockup
    
    def _generate_wireframe_svg(self, feature: str) -> str:
        """Generate a simple SVG wireframe representation"""
        # Simple wireframe SVG that can be rendered in frontend
        return f'''<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Header -->
  <rect x="0" y="0" width="800" height="60" fill="#1A1D29" stroke="#00FFFF" stroke-width="2"/>
  <text x="20" y="35" fill="#00FFFF" font-family="sans-serif" font-size="18" font-weight="bold">ProdigyPM</text>
  
  <!-- Sidebar -->
  <rect x="0" y="60" width="200" height="540" fill="#1A1D29" stroke="#00FFFF" stroke-width="2"/>
  <text x="20" y="100" fill="#FFFFFF" font-family="sans-serif" font-size="14">Navigation</text>
  <rect x="20" y="120" width="160" height="40" fill="#2A2E3A" rx="4"/>
  <rect x="20" y="170" width="160" height="40" fill="#2A2E3A" rx="4"/>
  <rect x="20" y="220" width="160" height="40" fill="#2A2E3A" rx="4"/>
  
  <!-- Main Content -->
  <rect x="200" y="60" width="600" height="540" fill="#0F1117" stroke="#00FFFF" stroke-width="2"/>
  <text x="220" y="100" fill="#FFFFFF" font-family="sans-serif" font-size="20" font-weight="bold">{feature[:50]}</text>
  
  <!-- Content Cards -->
  <rect x="220" y="120" width="560" height="120" fill="#1A1D29" stroke="#FF7A00" stroke-width="1" rx="8"/>
  <text x="240" y="150" fill="#FFFFFF" font-family="sans-serif" font-size="16">Component Area 1</text>
  
  <rect x="220" y="260" width="270" height="150" fill="#1A1D29" stroke="#FF7A00" stroke-width="1" rx="8"/>
  <text x="240" y="290" fill="#FFFFFF" font-family="sans-serif" font-size="14">Feature Block 1</text>
  
  <rect x="510" y="260" width="270" height="150" fill="#1A1D29" stroke="#FF7A00" stroke-width="1" rx="8"/>
  <text x="530" y="290" fill="#FFFFFF" font-family="sans-serif" font-size="14">Feature Block 2</text>
  
  <!-- Footer -->
  <rect x="220" y="430" width="560" height="50" fill="#1A1D29" stroke="#00FFFF" stroke-width="1" rx="4"/>
  <text x="240" y="460" fill="#00FFFF" font-family="sans-serif" font-size="12">Actions & Status</text>
</svg>'''

