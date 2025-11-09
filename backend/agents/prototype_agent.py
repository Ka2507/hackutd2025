"""
Prototype Agent - Integrates with Figma and creates design mockups

Enhanced to generate visual mockups and wireframes
"""
import logging
import sys
import os
from typing import Dict, Any, List
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
        
        # Check if user explicitly requested colors
        color_request_match = None
        import re
        hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', feature_description)
        color_words = re.findall(r'\b(blue|green|red|purple|pink|orange|yellow|cyan|teal|indigo|violet|magenta)\b', feature_description.lower())
        
        # Determine contextual color suggestions
        color_suggestions = self._generate_color_scheme(feature_description)
        
        # Use AI to generate design concept with component structure
        prompt = f"""You are a UX/UI designer creating a mockup for: {feature_description}

CRITICAL COLOR REQUIREMENTS:
- Choose colors that match the feature's domain and purpose
- PRIMARY and ACCENT colors MUST be DIFFERENT and complementary
- DO NOT use the same accent color for every design
- Consider the psychological impact of colors for this specific use case

{f"User explicitly requested colors: {', '.join(hex_colors)}" if hex_colors else f"Suggested colors for this domain: Primary={color_suggestions[0]}, Accent={color_suggestions[1]}"}

Provide a detailed design specification with:

1. Screen Title/Name
2. Layout Type (dashboard, form, list, detail view, etc.)
3. Exactly 5-7 Key UI Components with:
   - Component type (header, sidebar, card, form, table, chart, button, etc.)
   - Component purpose/content
   - Positioning (top, left, center, right, bottom)
4. Primary Color - MUST be a 6-digit hex code that fits the feature domain
5. Accent Color - MUST be a DIFFERENT 6-digit hex code that complements primary

Format your response EXACTLY as:
SCREEN: [name]
LAYOUT: [type]
COMPONENTS:
- [type]: [purpose] - [position]
- [type]: [purpose] - [position]
...
PRIMARY_COLOR: #[EXACTLY 6 HEX DIGITS]
ACCENT_COLOR: #[EXACTLY 6 HEX DIGITS - MUST BE DIFFERENT FROM PRIMARY]
INTERACTION: [description]

Then provide a narrative description of the design concept."""
        
        design_concept = await self._call_llm(prompt, use_cache=False)
        
        # Parse AI response for components and colors
        components_list = []
        primary_color = None
        accent_color = None
        screen_name = "Main Screen"
        
        # Try to extract structured info from AI response
        import re
        lines = design_concept.split('\n')
        for line in lines:
            line_upper = line.upper().strip()
            
            if line.startswith('SCREEN:'):
                screen_name = line.replace('SCREEN:', '').strip()
                
            # Parse PRIMARY_COLOR (case-insensitive)
            if line_upper.startswith('PRIMARY_COLOR:') or line_upper.startswith('PRIMARY COLOR:'):
                color_text = line.split(':', 1)[1].strip() if ':' in line else line
                hex_match = re.search(r'#[0-9A-Fa-f]{6}', color_text)
                if hex_match:
                    primary_color = hex_match.group(0).upper()
                    logger.info(f"✅ Parsed PRIMARY_COLOR: {primary_color}")
                    
            # Parse ACCENT_COLOR (case-insensitive, multiple variations)
            if (line_upper.startswith('ACCENT_COLOR:') or 
                line_upper.startswith('ACCENT COLOR:') or
                line_upper.startswith('SECONDARY_COLOR:') or
                line_upper.startswith('SECONDARY COLOR:')):
                color_text = line.split(':', 1)[1].strip() if ':' in line else line
                hex_match = re.search(r'#[0-9A-Fa-f]{6}', color_text)
                if hex_match:
                    accent_color = hex_match.group(0).upper()
                    logger.info(f"✅ Parsed ACCENT_COLOR: {accent_color}")
                    
            # Parse component lines
            if line.strip().startswith('-') and ':' in line:
                parts = line.strip()[1:].split(':', 1)
                if len(parts) == 2:
                    comp_type = parts[0].strip()
                    comp_rest = parts[1].strip()
                    comp_desc = comp_rest.split('-')[0].strip() if '-' in comp_rest else comp_rest
                    if comp_type.lower() not in ['primary', 'accent', 'secondary']:  # Skip if it's a color line
                        components_list.append({
                            "type": comp_type,
                            "content": comp_desc
                        })
        
        # Log what AI provided
        logger.info(f"🔍 AI provided - Primary: {primary_color}, Accent: {accent_color}")
        
        # Generate dynamic color scheme based on feature if AI didn't provide BOTH
        if not primary_color or not accent_color:
            # Check if user provided hex colors directly in request
            import re
            hex_colors_in_request = re.findall(r'#[0-9A-Fa-f]{6}', feature_description)
            
            if len(hex_colors_in_request) >= 2:
                # User provided colors directly
                if not primary_color:
                    primary_color = hex_colors_in_request[0].upper()
                if not accent_color:
                    accent_color = hex_colors_in_request[1].upper()
                logger.info(f"🎨 Using user-provided colors: {primary_color}, {accent_color}")
                
            elif len(hex_colors_in_request) == 1:
                # User provided one color
                if not primary_color:
                    primary_color = hex_colors_in_request[0].upper()
                if not accent_color:
                    accent_color = self._generate_complementary_color(primary_color)
                logger.info(f"🎨 User color + complementary: {primary_color}, {accent_color}")
                
            else:
                # Generate based on feature description (contextual)
                fallback_primary, fallback_accent = self._generate_color_scheme(feature_description)
                if not primary_color:
                    primary_color = fallback_primary
                if not accent_color:
                    accent_color = fallback_accent
                logger.info(f"🎨 Using contextual fallback: {primary_color}, {accent_color}")
        
        # Safety check: If AI keeps using #F97316 as accent, override with contextual scheme
        if accent_color and accent_color.upper() == "#F97316" and primary_color:
            # AI defaulted to orange - use our contextual scheme instead
            _, contextual_accent = self._generate_color_scheme(feature_description)
            if contextual_accent != "#FF7A00":  # If contextual is also not orange
                accent_color = contextual_accent
                logger.info(f"⚠️ AI used default orange, overriding with contextual accent: {accent_color}")
        
        logger.info(f"🎨 FINAL COLORS - Primary: {primary_color}, Accent: {accent_color}")
        
        # If no components extracted, create based on feature description
        if not components_list:
            # Infer components from feature description
            desc_lower = feature_description.lower()
            if 'dashboard' in desc_lower or 'analytics' in desc_lower:
                components_list = [
                    {"type": "header", "content": "Navigation & metrics overview"},
                    {"type": "sidebar", "content": "Quick access menu"},
                    {"type": "chart", "content": "Analytics visualization"},
                    {"type": "card", "content": "Key performance indicators"},
                    {"type": "table", "content": "Recent activity data"}
                ]
            elif 'login' in desc_lower or 'auth' in desc_lower or 'sign' in desc_lower:
                components_list = [
                    {"type": "header", "content": "Logo and branding"},
                    {"type": "form", "content": "Login form with email/password"},
                    {"type": "button", "content": "Sign in button"},
                    {"type": "link", "content": "Forgot password link"},
                    {"type": "footer", "content": "Terms and privacy links"}
                ]
            elif 'settings' in desc_lower or 'profile' in desc_lower:
                components_list = [
                    {"type": "header", "content": "Settings navigation"},
                    {"type": "sidebar", "content": "Settings categories"},
                    {"type": "form", "content": "Settings form fields"},
                    {"type": "button", "content": "Save changes button"},
                    {"type": "toggle", "content": "Preference toggles"}
                ]
            elif 'chat' in desc_lower or 'message' in desc_lower:
                components_list = [
                    {"type": "header", "content": "Chat header with user info"},
                    {"type": "sidebar", "content": "Conversations list"},
                    {"type": "messages", "content": "Message thread display"},
                    {"type": "input", "content": "Message input field"},
                    {"type": "button", "content": "Send message button"}
                ]
            else:
                components_list = [
                    {"type": "header", "content": f"Header for {feature_description[:30]}"},
                    {"type": "content", "content": "Main content area"},
                    {"type": "sidebar", "content": "Navigation panel"},
                    {"type": "action", "content": "Primary action buttons"},
                    {"type": "footer", "content": "Status and info"}
                ]
        
        # Generate mockup structure with parsed data
        mockup = {
            "title": f"Mockup: {feature_description[:100]}",
            "screens": [
                {
                    "name": screen_name,
                    "layout": f"Custom layout for {feature_description[:50]}",
                    "components": components_list,
                    "wireframe_svg": self._generate_wireframe_svg(feature_description, components_list, primary_color, accent_color),
                    "notes": f"Design tailored specifically for: {feature_description[:100]}"
                }
            ],
            "design_concept": design_concept,
            "color_palette": {
                "primary": primary_color,
                "secondary": accent_color,
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
    
    def _generate_color_scheme(self, feature_description: str) -> tuple:
        """
        Generate dynamic color scheme based on feature description
        
        Returns:
            (primary_color, accent_color) as hex strings
        """
        desc_lower = feature_description.lower()
        
        # Color schemes based on context and keywords
        color_schemes = {
            # Finance/Banking - Professional blues
            ('financial', 'banking', 'payment', 'transaction', 'money'): ("#2563EB", "#10B981"),
            
            # Health/Medical - Calming greens and blues
            ('health', 'medical', 'healthcare', 'wellness', 'fitness'): ("#10B981", "#3B82F6"),
            
            # Social/Communication - Friendly purples
            ('social', 'chat', 'message', 'community', 'communication'): ("#8B5CF6", "#EC4899"),
            
            # Analytics/Data - Professional cyan/blue
            ('analytics', 'dashboard', 'data', 'metrics', 'insights'): ("#06B6D4", "#F59E0B"),
            
            # Security/Auth - Bold red/orange
            ('security', 'auth', 'login', 'password', 'encryption'): ("#EF4444", "#F97316"),
            
            # E-commerce/Shopping - Vibrant orange/purple
            ('shop', 'ecommerce', 'store', 'product', 'cart'): ("#F97316", "#A855F7"),
            
            # Education/Learning - Warm yellow/blue
            ('education', 'learning', 'course', 'student', 'teach'): ("#F59E0B", "#3B82F6"),
            
            # Creative/Design - Artistic pink/purple
            ('design', 'creative', 'art', 'photo', 'media'): ("#EC4899", "#8B5CF6"),
            
            # Settings/Admin - Neutral gray/blue
            ('settings', 'admin', 'config', 'preferences', 'account'): ("#6B7280", "#3B82F6"),
            
            # Default - Original ProdPlex colors
            ('default',): ("#00FFFF", "#FF7A00")
        }
        
        # Match keywords to color scheme
        for keywords, (primary, accent) in color_schemes.items():
            if any(keyword in desc_lower for keyword in keywords):
                return (primary, accent)
        
        # Fallback: Generate pseudo-random colors based on description hash
        hash_val = hash(feature_description) % 7
        fallback_schemes = [
            ("#00FFFF", "#FF7A00"),  # Cyan/Orange (default)
            ("#8B5CF6", "#EC4899"),  # Purple/Pink
            ("#10B981", "#F59E0B"),  # Green/Yellow
            ("#3B82F6", "#F97316"),  # Blue/Orange
            ("#EF4444", "#FBBF24"),  # Red/Yellow
            ("#06B6D4", "#A855F7"),  # Cyan/Purple
            ("#F59E0B", "#10B981"),  # Yellow/Green
        ]
        
        return fallback_schemes[hash_val]
    
    def _generate_complementary_color(self, hex_color: str) -> str:
        """Generate a complementary/contrasting color"""
        # Remove # if present
        hex_color = hex_color.replace('#', '')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Generate complementary (simple approach: rotate hue by 180°)
        # For simplicity, just invert and adjust
        comp_r = 255 - r
        comp_g = 255 - g
        comp_b = 255 - b
        
        # Ensure it's vibrant enough (boost saturation)
        max_val = max(comp_r, comp_g, comp_b)
        if max_val < 200:
            factor = 220 / max_val
            comp_r = min(255, int(comp_r * factor))
            comp_g = min(255, int(comp_g * factor))
            comp_b = min(255, int(comp_b * factor))
        
        return f"#{comp_r:02X}{comp_g:02X}{comp_b:02X}"
    
    def _generate_wireframe_svg(self, feature: str, components: List[Dict[str, Any]], primary_color: str = "#00FFFF", accent_color: str = "#FF7A00") -> str:
        """Generate a dynamic SVG wireframe based on components"""
        
        # Start SVG
        svg_parts = [f'<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">']
        
        # Add title/feature name at top
        svg_parts.append(f'  <!-- Feature: {feature[:50]} -->')
        
        # Dynamic component rendering
        y_position = 0
        
        for idx, comp in enumerate(components[:7]):  # Max 7 components to fit
            comp_type = comp.get('type', 'box').lower()
            comp_content = comp.get('content', 'Component')[:40]
            
            if comp_type in ['header', 'navbar', 'navigation']:
                # Header at top
                svg_parts.append(f'  <rect x="0" y="{y_position}" width="800" height="60" fill="#1A1D29" stroke="{primary_color}" stroke-width="2"/>')
                svg_parts.append(f'  <text x="20" y="{y_position + 35}" fill="{primary_color}" font-family="sans-serif" font-size="16" font-weight="bold">{comp_content}</text>')
                y_position += 70
                
            elif comp_type in ['sidebar', 'menu', 'nav']:
                # Sidebar
                svg_parts.append(f'  <rect x="0" y="{y_position}" width="180" height="300" fill="#1A1D29" stroke="{primary_color}" stroke-width="1"/>')
                svg_parts.append(f'  <text x="15" y="{y_position + 30}" fill="#FFFFFF" font-family="sans-serif" font-size="13">{comp_content}</text>')
                for i in range(3):
                    svg_parts.append(f'  <rect x="15" y="{y_position + 50 + i*50}" width="150" height="35" fill="#2A2E3A" rx="4"/>')
                
            elif comp_type in ['form', 'input']:
                # Form elements
                svg_parts.append(f'  <rect x="200" y="{y_position}" width="580" height="180" fill="#1A1D29" stroke="{accent_color}" stroke-width="1" rx="8"/>')
                svg_parts.append(f'  <text x="220" y="{y_position + 30}" fill="#FFFFFF" font-family="sans-serif" font-size="14">{comp_content}</text>')
                # Input fields
                svg_parts.append(f'  <rect x="220" y="{y_position + 50}" width="540" height="35" fill="#0F1117" stroke="#444" stroke-width="1" rx="4"/>')
                svg_parts.append(f'  <rect x="220" y="{y_position + 100}" width="540" height="35" fill="#0F1117" stroke="#444" stroke-width="1" rx="4"/>')
                y_position += 200
                
            elif comp_type in ['chart', 'graph', 'analytics']:
                # Chart visualization
                svg_parts.append(f'  <rect x="200" y="{y_position}" width="380" height="200" fill="#1A1D29" stroke="{accent_color}" stroke-width="1" rx="8"/>')
                svg_parts.append(f'  <text x="220" y="{y_position + 25}" fill="#FFFFFF" font-family="sans-serif" font-size="12">{comp_content}</text>')
                # Simple bar chart representation
                for i in range(5):
                    height = 40 + (i * 20)
                    svg_parts.append(f'  <rect x="{220 + i*70}" y="{y_position + 180 - height}" width="50" height="{height}" fill="{primary_color}" opacity="0.7"/>')
                
            elif comp_type in ['card', 'panel']:
                # Card component
                width = 270 if idx % 2 == 0 else 270
                x_pos = 200 if idx % 2 == 0 else 510
                svg_parts.append(f'  <rect x="{x_pos}" y="{y_position}" width="{width}" height="120" fill="#1A1D29" stroke="{accent_color}" stroke-width="1" rx="8"/>')
                svg_parts.append(f'  <text x="{x_pos + 20}" y="{y_position + 30}" fill="#FFFFFF" font-family="sans-serif" font-size="13">{comp_content}</text>')
                if idx % 2 == 1:
                    y_position += 140
                
            elif comp_type in ['table', 'list']:
                # Table/List
                svg_parts.append(f'  <rect x="200" y="{y_position}" width="580" height="200" fill="#1A1D29" stroke="{primary_color}" stroke-width="1" rx="6"/>')
                svg_parts.append(f'  <text x="220" y="{y_position + 25}" fill="#FFFFFF" font-family="sans-serif" font-size="12">{comp_content}</text>')
                # Table rows
                for i in range(4):
                    svg_parts.append(f'  <rect x="220" y="{y_position + 40 + i*40}" width="540" height="30" fill="#2A2E3A" opacity="0.5"/>')
                y_position += 220
                
            elif comp_type in ['button', 'action', 'cta']:
                # Button
                svg_parts.append(f'  <rect x="200" y="{y_position}" width="200" height="50" fill="{primary_color}" rx="8"/>')
                svg_parts.append(f'  <text x="300" y="{y_position + 32}" fill="#0F1117" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">{comp_content[:20]}</text>')
                y_position += 70
                
            else:
                # Generic content block
                svg_parts.append(f'  <rect x="200" y="{y_position}" width="580" height="100" fill="#1A1D29" stroke="{accent_color}" stroke-width="1" rx="6"/>')
                svg_parts.append(f'  <text x="220" y="{y_position + 30}" fill="#FFFFFF" font-family="sans-serif" font-size="13">{comp_content}</text>')
                y_position += 120
        
        # Close SVG
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)

