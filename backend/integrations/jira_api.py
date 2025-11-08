"""
Jira API Integration - Mock implementation for MVP
In production, use python-jira library
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger


class JiraAPI:
    """Mock Jira API integration"""
    
    def __init__(self):
        self.base_url = settings.JIRA_BASE_URL or "https://your-domain.atlassian.net"
        self.api_token = settings.JIRA_API_TOKEN
        self.connected = bool(self.api_token)
        
        if not self.connected:
            logger.warning("Jira API token not configured. Using mock data.")
    
    async def get_sprint_data(self, sprint_id: str) -> Dict[str, Any]:
        """Get sprint data from Jira"""
        logger.info(f"Fetching sprint data for {sprint_id}")
        
        # Mock sprint data
        return {
            "id": sprint_id,
            "name": "Sprint 1",
            "state": "active",
            "startDate": "2025-10-28",
            "endDate": "2025-11-08",
            "goal": "Deliver MVP with core agent functionality",
            "issues": [
                {
                    "key": "PROD-101",
                    "summary": "Build agent dashboard",
                    "status": "Done",
                    "assignee": "dev1",
                    "storyPoints": 8
                },
                {
                    "key": "PROD-102",
                    "summary": "Implement chat interface",
                    "status": "Done",
                    "assignee": "dev2",
                    "storyPoints": 5
                },
                {
                    "key": "PROD-103",
                    "summary": "Automated sprint summaries",
                    "status": "In Progress",
                    "assignee": "dev1",
                    "storyPoints": 13
                }
            ],
            "completedPoints": 13,
            "totalPoints": 26
        }
    
    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Story",
        story_points: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a Jira issue"""
        logger.info(f"Creating Jira issue: {summary}")
        
        # Mock issue creation
        issue_key = f"{project_key}-{hash(summary) % 1000}"
        
        return {
            "key": issue_key,
            "id": str(hash(summary)),
            "self": f"{self.base_url}/rest/api/3/issue/{issue_key}",
            "summary": summary,
            "description": description,
            "issueType": issue_type,
            "storyPoints": story_points,
            "status": "To Do",
            "created": "2025-11-08T12:00:00.000Z"
        }
    
    async def bulk_create_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple Jira issues"""
        logger.info(f"Bulk creating {len(issues)} Jira issues")
        
        results = []
        for issue in issues:
            result = await self.create_issue(
                project_key=issue.get("project_key", "PROD"),
                summary=issue.get("summary", ""),
                description=issue.get("description", ""),
                issue_type=issue.get("issue_type", "Story"),
                story_points=issue.get("story_points")
            )
            results.append(result)
        
        return results
    
    async def get_project_issues(
        self,
        project_key: str,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get issues for a project"""
        logger.info(f"Fetching issues for project {project_key}")
        
        # Mock project issues
        all_issues = [
            {
                "key": "PROD-101",
                "summary": "Build agent dashboard",
                "status": "Done",
                "priority": "High",
                "assignee": "dev1",
                "storyPoints": 8
            },
            {
                "key": "PROD-102",
                "summary": "Implement chat interface",
                "status": "Done",
                "priority": "High",
                "assignee": "dev2",
                "storyPoints": 5
            },
            {
                "key": "PROD-103",
                "summary": "Automated sprint summaries",
                "status": "In Progress",
                "priority": "Medium",
                "assignee": "dev1",
                "storyPoints": 13
            },
            {
                "key": "PROD-104",
                "summary": "Nemotron integration",
                "status": "To Do",
                "priority": "High",
                "assignee": None,
                "storyPoints": 8
            }
        ]
        
        if status:
            return [issue for issue in all_issues if issue["status"] == status]
        
        return all_issues
    
    async def update_issue_status(self, issue_key: str, status: str) -> Dict[str, Any]:
        """Update issue status"""
        logger.info(f"Updating {issue_key} status to {status}")
        
        return {
            "key": issue_key,
            "status": status,
            "updated": "2025-11-08T12:00:00.000Z"
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check Jira API health"""
        return {
            "connected": self.connected,
            "base_url": self.base_url,
            "status": "mock" if not self.connected else "connected"
        }


# Global instance
jira_api = JiraAPI()

