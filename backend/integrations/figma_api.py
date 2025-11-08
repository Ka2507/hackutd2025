"""
Figma API Integration - Mock implementation for MVP
In production, use Figma REST API
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger


class FigmaAPI:
    """Mock Figma API integration"""
    
    def __init__(self):
        self.access_token = settings.FIGMA_ACCESS_TOKEN
        self.connected = bool(self.access_token)
        
        if not self.connected:
            logger.warning("Figma access token not configured. Using mock data.")
    
    async def get_file(self, file_key: str) -> Dict[str, Any]:
        """Get Figma file data"""
        logger.info(f"Fetching Figma file: {file_key}")
        
        # Mock file data
        return {
            "name": "ProdigyPM Design System",
            "lastModified": "2025-11-08T12:00:00Z",
            "thumbnailUrl": f"https://figma.com/thumb/{file_key}",
            "version": "1.0.0",
            "document": {
                "id": file_key,
                "name": "ProdigyPM",
                "type": "DOCUMENT",
                "children": [
                    {
                        "id": "0:1",
                        "name": "Dashboard",
                        "type": "FRAME"
                    },
                    {
                        "id": "0:2",
                        "name": "Components",
                        "type": "FRAME"
                    }
                ]
            }
        }
    
    async def get_file_nodes(
        self,
        file_key: str,
        node_ids: List[str]
    ) -> Dict[str, Any]:
        """Get specific nodes from a Figma file"""
        logger.info(f"Fetching nodes from {file_key}: {node_ids}")
        
        # Mock node data
        return {
            "nodes": {
                node_id: {
                    "document": {
                        "id": node_id,
                        "name": f"Frame {node_id}",
                        "type": "FRAME"
                    },
                    "components": {},
                    "styles": {}
                }
                for node_id in node_ids
            }
        }
    
    async def get_images(
        self,
        file_key: str,
        node_ids: List[str],
        scale: float = 2.0,
        format: str = "png"
    ) -> Dict[str, Any]:
        """Export images from Figma"""
        logger.info(f"Exporting images from {file_key}")
        
        # Mock image URLs
        return {
            "err": None,
            "images": {
                node_id: f"https://figma.com/img/{file_key}/{node_id}.{format}"
                for node_id in node_ids
            }
        }
    
    async def get_comments(self, file_key: str) -> List[Dict[str, Any]]:
        """Get comments from a Figma file"""
        logger.info(f"Fetching comments from {file_key}")
        
        # Mock comments
        return [
            {
                "id": "1",
                "message": "Love the dashboard layout!",
                "user": {
                    "handle": "designer1",
                    "img_url": "https://figma.com/avatar/1"
                },
                "created_at": "2025-11-07T10:00:00Z",
                "resolved_at": None
            },
            {
                "id": "2",
                "message": "Can we make the agent cards bigger?",
                "user": {
                    "handle": "pm1",
                    "img_url": "https://figma.com/avatar/2"
                },
                "created_at": "2025-11-07T14:00:00Z",
                "resolved_at": "2025-11-08T09:00:00Z"
            }
        ]
    
    async def post_comment(
        self,
        file_key: str,
        message: str,
        client_meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Post a comment to a Figma file"""
        logger.info(f"Posting comment to {file_key}")
        
        return {
            "id": str(hash(message) % 10000),
            "message": message,
            "user": {
                "handle": "prodigypm_bot",
                "img_url": "https://figma.com/avatar/bot"
            },
            "created_at": "2025-11-08T12:00:00Z"
        }
    
    async def get_team_projects(self, team_id: str) -> List[Dict[str, Any]]:
        """Get projects from a team"""
        logger.info(f"Fetching projects for team {team_id}")
        
        # Mock projects
        return [
            {
                "id": "1",
                "name": "ProdigyPM MVP",
                "files": [
                    {
                        "key": "abc123",
                        "name": "Dashboard Designs",
                        "thumbnail_url": "https://figma.com/thumb/abc123"
                    },
                    {
                        "key": "def456",
                        "name": "Component Library",
                        "thumbnail_url": "https://figma.com/thumb/def456"
                    }
                ]
            }
        ]
    
    async def create_prototype_link(
        self,
        file_key: str,
        node_id: str
    ) -> Dict[str, Any]:
        """Create a shareable prototype link"""
        logger.info(f"Creating prototype link for {file_key}/{node_id}")
        
        return {
            "url": f"https://www.figma.com/proto/{file_key}/{node_id}",
            "expires_at": None
        }
    
    async def get_design_tokens(self, file_key: str) -> Dict[str, Any]:
        """Extract design tokens from Figma file"""
        logger.info(f"Extracting design tokens from {file_key}")
        
        # Mock design tokens
        return {
            "colors": {
                "primary": {
                    "charcoal": "#0F1117",
                    "neon_cyan": "#00FFFF",
                    "soft_orange": "#FF7A00"
                }
            },
            "typography": {
                "heading": "Orbitron",
                "body": "Inter"
            },
            "spacing": [0, 4, 8, 12, 16, 24, 32, 48, 64],
            "borderRadius": [0, 4, 8, 12, 16]
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check Figma API health"""
        return {
            "connected": self.connected,
            "status": "mock" if not self.connected else "connected"
        }


# Global instance
figma_api = FigmaAPI()

