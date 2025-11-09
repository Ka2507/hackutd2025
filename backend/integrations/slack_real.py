"""
Slack API Integration for Notifications and Reports

Real Slack API integration for Automation Agent
"""
import logging
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import settings

logger = logging.getLogger(__name__)

# Try to import Slack SDK
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    logger.warning("slack-sdk not installed. Install with: pip install slack-sdk")


class SlackIntegration:
    """Real Slack API integration"""
    
    def __init__(self):
        """Initialize Slack client"""
        self.bot_token = settings.slack_bot_token
        self.client = None
        self.connected = False
        
        if self.bot_token and SLACK_AVAILABLE:
            try:
                self.client = WebClient(token=self.bot_token)
                # Test connection
                auth_test = self.client.auth_test()
                self.connected = auth_test.get("ok", False)
                logger.info(f"✅ Connected to Slack workspace: {auth_test.get('team')}")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Slack: {e}")
                self.connected = False
        else:
            logger.warning("⚠️ Slack not configured. Using mock data.")
    
    async def send_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        logger.info(f"Sending message to {channel}")
        
        if self.connected:
            try:
                result = self.client.chat_postMessage(
                    channel=channel,
                    text=text,
                    blocks=blocks
                )
                return {
                    "success": True,
                    "ts": result.get("ts"),
                    "channel": result.get("channel")
                }
            except Exception as e:
                logger.error(f"❌ Error sending message: {e}")
                return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "ts": "mock-timestamp",
                "channel": channel,
                "mock": True
            }
    
    async def send_sprint_report(
        self,
        channel: str,
        sprint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send formatted sprint report to Slack"""
        logger.info(f"Sending sprint report to {channel}")
        
        stats = sprint_data.get("statistics", {})
        
        # Build message blocks
        text = f"🚀 Sprint Report"
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚀 Sprint Report - Sprint #{sprint_data.get('sprint_id', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Issues:*\n{stats.get('total_issues', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Story Points:*\n{stats.get('total_points', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Completed:*\n{stats.get('completed_points', 0)} pts"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Progress:*\n{stats.get('completion_percentage', 0):.1f}%"
                    }
                ]
            }
        ]
        
        return await self.send_message(channel, text, blocks)
    
    async def send_prd_notification(
        self,
        channel: str,
        prd_title: str,
        prd_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send PRD creation notification"""
        logger.info(f"Sending PRD notification to {channel}")
        
        text = f"📄 New PRD Created: {prd_title}"
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📄 New PRD Created"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{prd_title}*"
                }
            }
        ]
        
        if prd_url:
            blocks.append({
                "type": "actions",
                "elements": [{
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View PRD"
                    },
                    "url": prd_url
                }]
            })
        
        return await self.send_message(channel, text, blocks)
    
    def health_check(self) -> Dict[str, Any]:
        """Check Slack API health"""
        return {
            "connected": self.connected,
            "sdk_available": SLACK_AVAILABLE,
            "status": "connected" if self.connected else ("mock" if SLACK_AVAILABLE else "no-library")
        }


# Global instance
slack_integration = SlackIntegration()

