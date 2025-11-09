"""
Figma API Integration for Design Generation

Real Figma API integration for Prototype Agent
"""
import logging
import requests
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import settings

logger = logging.getLogger(__name__)


class FigmaIntegration:
    """Real Figma API integration"""
    
    def __init__(self):
        """Initialize Figma connection"""
        self.access_token = settings.figma_access_token
        self.base_url = "https://api.figma.com/v1"
        self.connected = bool(self.access_token)
        
        if self.connected:
            logger.info("✅ Figma API token configured")
        else:
            logger.warning("⚠️ Figma not configured. Using mock data.")
    
    async def get_file(self, file_key: str) -> Dict[str, Any]:
        """Get Figma file"""
        logger.info(f"Fetching Figma file: {file_key}")
        
        if self.connected:
            try:
                headers = {"X-Figma-Token": self.access_token}
                response = requests.get(f"{self.base_url}/files/{file_key}", headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"❌ Error fetching Figma file: {e}")
                return self._mock_file_data(file_key)
        else:
            return self._mock_file_data(file_key)
    
    async def create_comment(
        self,
        file_key: str,
        message: str,
        client_meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Post comment to Figma file"""
        logger.info(f"Posting comment to {file_key}")
        
        if self.connected:
            try:
                headers = {"X-Figma-Token": self.access_token}
                data = {"message": message}
                if client_meta:
                    data["client_meta"] = client_meta
                
                response = requests.post(
                    f"{self.base_url}/files/{file_key}/comments",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"❌ Error posting comment: {e}")
                return {"success": False, "error": str(e)}
        else:
            return {
                "id": "mock-comment-id",
                "message": message,
                "mock": True
            }
    
    async def export_images(
        self,
        file_key: str,
        node_ids: List[str],
        scale: float = 2.0,
        format: str = "png"
    ) -> Dict[str, str]:
        """Export images from Figma"""
        logger.info(f"Exporting {len(node_ids)} images from {file_key}")
        
        if self.connected:
            try:
                headers = {"X-Figma-Token": self.access_token}
                params = {
                    "ids": ",".join(node_ids),
                    "scale": scale,
                    "format": format
                }
                response = requests.get(
                    f"{self.base_url}/images/{file_key}",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json().get("images", {})
            except Exception as e:
                logger.error(f"❌ Error exporting images: {e}")
                return {}
        else:
            return {node_id: f"https://figma.com/mock/{file_key}/{node_id}.{format}" for node_id in node_ids}
    
    def health_check(self) -> Dict[str, Any]:
        """Check Figma API health"""
        return {
            "connected": self.connected,
            "status": "connected" if self.connected else "mock"
        }
    
    def _mock_file_data(self, file_key: str) -> Dict[str, Any]:
        """Generate mock file data"""
        return {
            "name": "ProdigyPM Designs",
            "lastModified": "2025-11-08T12:00:00Z",
            "thumbnailUrl": f"https://figma.com/thumb/{file_key}",
            "document": {
                "id": file_key,
                "name": "ProdigyPM",
                "children": [
                    {"id": "1:1", "name": "Dashboard", "type": "FRAME"},
                    {"id": "1:2", "name": "Components", "type": "FRAME"}
                ]
            },
            "mock": True
        }


# Global instance
figma_integration = FigmaIntegration()

