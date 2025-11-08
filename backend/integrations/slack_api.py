"""
Slack API Integration - Mock implementation for MVP
In production, use slack-sdk library
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger


class SlackAPI:
    """Mock Slack API integration"""
    
    def __init__(self):
        self.bot_token = settings.slack_bot_token
        self.connected = bool(self.bot_token)
        
        if not self.connected:
            logger.warning("Slack bot token not configured. Using mock data.")
    
    async def post_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict]] = None,
        thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """Post a message to Slack"""
        logger.info(f"Posting message to #{channel}: {text[:50]}...")
        
        # Mock message post
        return {
            "ok": True,
            "channel": channel,
            "ts": "1699459200.123456",
            "message": {
                "text": text,
                "blocks": blocks,
                "user": "U0123ABCD",
                "bot_id": "B0123ABCD",
                "type": "message",
                "thread_ts": thread_ts
            }
        }
    
    async def post_sprint_summary(
        self,
        channel: str,
        sprint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Post sprint summary with rich formatting"""
        logger.info(f"Posting sprint summary to #{channel}")
        
        # Create rich Slack blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Sprint Summary: {sprint_data.get('sprint_id', 'N/A')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Velocity:*\n{sprint_data.get('metrics', {}).get('velocity', 0)} points"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Completion:*\n{sprint_data.get('metrics', {}).get('completion_rate', 0)}%"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Key Accomplishments:*\n" + "\n".join(
                        sprint_data.get('accomplishments', [])[:5]
                    )
                }
            }
        ]
        
        return await self.post_message(
            channel=channel,
            text=f"Sprint {sprint_data.get('sprint_id')} Summary",
            blocks=blocks
        )
    
    async def post_agent_update(
        self,
        channel: str,
        agent_name: str,
        task: str,
        status: str,
        result: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Post agent status update"""
        logger.info(f"Posting agent update to #{channel}: {agent_name} - {status}")
        
        status_emoji = {
            "started": "🚀",
            "running": "⚡",
            "completed": "✅",
            "failed": "❌"
        }.get(status, "ℹ️")
        
        text = f"{status_emoji} *{agent_name}* {status}\n_{task}_"
        
        if result and status == "completed":
            text += f"\n\n*Key Results:*\n• {result.get('summary', 'Task completed')}"
        
        return await self.post_message(channel=channel, text=text)
    
    async def create_channel(self, name: str, is_private: bool = False) -> Dict[str, Any]:
        """Create a Slack channel"""
        logger.info(f"Creating {'private' if is_private else 'public'} channel: {name}")
        
        return {
            "ok": True,
            "channel": {
                "id": f"C{hash(name) % 10000000}",
                "name": name,
                "is_private": is_private,
                "created": 1699459200
            }
        }
    
    async def list_channels(self) -> List[Dict[str, Any]]:
        """List Slack channels"""
        logger.info("Listing Slack channels")
        
        # Mock channels
        return [
            {
                "id": "C0123ABCD",
                "name": "product-updates",
                "is_member": True,
                "num_members": 25
            },
            {
                "id": "C0123ABCE",
                "name": "daily-updates",
                "is_member": True,
                "num_members": 15
            },
            {
                "id": "C0123ABCF",
                "name": "agent-alerts",
                "is_member": True,
                "num_members": 8
            }
        ]
    
    async def upload_file(
        self,
        channels: str,
        file_path: str,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a file to Slack"""
        logger.info(f"Uploading file {file_path} to {channels}")
        
        return {
            "ok": True,
            "file": {
                "id": f"F{hash(file_path) % 10000000}",
                "title": title or file_path,
                "name": file_path.split("/")[-1],
                "mimetype": "application/pdf",
                "permalink": f"https://files.slack.com/files-pri/T0123/F{hash(file_path)}"
            }
        }
    
    async def send_notification(
        self,
        channel: str,
        title: str,
        message: str,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Send a formatted notification"""
        logger.info(f"Sending {priority} notification to #{channel}")
        
        color = {
            "low": "#36a64f",
            "normal": "#439FE0",
            "high": "#ff9900",
            "critical": "#ff0000"
        }.get(priority, "#439FE0")
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\n{message}"
                }
            }
        ]
        
        return await self.post_message(channel=channel, text=title, blocks=blocks)
    
    def health_check(self) -> Dict[str, Any]:
        """Check Slack API health"""
        return {
            "connected": self.connected,
            "status": "mock" if not self.connected else "connected"
        }


# Global instance
slack_api = SlackAPI()

