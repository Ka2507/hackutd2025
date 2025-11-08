"""
Reddit API Integration - Mock implementation for MVP
In production, use PRAW (Python Reddit API Wrapper)
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger


class RedditAPI:
    """Mock Reddit API integration"""
    
    def __init__(self):
        self.client_id = settings.reddit_client_id
        self.client_secret = settings.reddit_client_secret
        self.connected = bool(self.client_id and self.client_secret)
        
        if not self.connected:
            logger.warning("Reddit API credentials not configured. Using mock data.")
    
    async def search_subreddit(
        self,
        subreddit: str,
        query: str,
        sort: str = "relevance",
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Search posts in a subreddit"""
        logger.info(f"Searching r/{subreddit} for: {query}")
        
        # Mock search results
        return [
            {
                "id": "abc123",
                "title": "AI tools are transforming product management",
                "selftext": "I've been using AI agents to help with planning and they save me 10+ hours per week. Has anyone else tried this?",
                "score": 245,
                "num_comments": 67,
                "author": "pm_enthusiast",
                "created_utc": 1699372800,
                "url": f"https://reddit.com/r/{subreddit}/comments/abc123",
                "subreddit": subreddit
            },
            {
                "id": "def456",
                "title": "Looking for PM tools with AI capabilities",
                "selftext": "What are the best AI-powered tools for product managers? Need something for research and planning.",
                "score": 189,
                "num_comments": 43,
                "author": "tech_pm",
                "created_utc": 1699286400,
                "url": f"https://reddit.com/r/{subreddit}/comments/def456",
                "subreddit": subreddit
            },
            {
                "id": "ghi789",
                "title": "The future of product management is AI-first",
                "selftext": "Change my mind: Within 2 years, every PM will have an AI copilot. The ones who don't will be left behind.",
                "score": 512,
                "num_comments": 156,
                "author": "future_thinking",
                "created_utc": 1699200000,
                "url": f"https://reddit.com/r/{subreddit}/comments/ghi789",
                "subreddit": subreddit
            }
        ]
    
    async def get_hot_posts(
        self,
        subreddit: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get hot posts from a subreddit"""
        logger.info(f"Fetching hot posts from r/{subreddit}")
        
        # Mock hot posts
        return await self.search_subreddit(subreddit, "product management", limit=limit)
    
    async def get_post_comments(
        self,
        post_id: str,
        sort: str = "top",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get comments from a post"""
        logger.info(f"Fetching comments for post {post_id}")
        
        # Mock comments
        return [
            {
                "id": "c1",
                "body": "This is exactly what I've been looking for. AI agents could revolutionize PM workflows.",
                "score": 45,
                "author": "commenter1",
                "created_utc": 1699373000,
                "replies": []
            },
            {
                "id": "c2",
                "body": "I'm skeptical. AI can help but won't replace the strategic thinking PMs need to do.",
                "score": 32,
                "author": "commenter2",
                "created_utc": 1699373200,
                "replies": [
                    {
                        "id": "c2a",
                        "body": "I don't think anyone is saying it will replace PMs, just augment their capabilities.",
                        "score": 18,
                        "author": "commenter3",
                        "created_utc": 1699373400
                    }
                ]
            },
            {
                "id": "c3",
                "body": "Anyone tried ProdigyPM? Saw it mentioned on Product Hunt.",
                "score": 12,
                "author": "commenter4",
                "created_utc": 1699373600,
                "replies": []
            }
        ]
    
    async def analyze_sentiment(
        self,
        subreddit: str,
        query: str
    ) -> Dict[str, Any]:
        """Analyze sentiment of posts/comments"""
        logger.info(f"Analyzing sentiment for '{query}' in r/{subreddit}")
        
        posts = await self.search_subreddit(subreddit, query)
        
        # Mock sentiment analysis
        return {
            "query": query,
            "subreddit": subreddit,
            "posts_analyzed": len(posts),
            "overall_sentiment": "positive",
            "sentiment_scores": {
                "positive": 0.65,
                "neutral": 0.25,
                "negative": 0.10
            },
            "common_themes": [
                "Time savings with AI tools",
                "Need for better PM automation",
                "Interest in AI copilots",
                "Privacy concerns with cloud AI"
            ],
            "top_pain_points": [
                "Too much time on repetitive tasks",
                "Difficulty synthesizing user feedback",
                "Context switching between tools"
            ],
            "sample_quotes": [
                "AI agents could revolutionize PM workflows",
                "I spend 50% of my time on admin work",
                "Need an AI copilot for product decisions"
            ]
        }
    
    async def get_trending_topics(
        self,
        subreddit: str
    ) -> List[Dict[str, Any]]:
        """Get trending topics in a subreddit"""
        logger.info(f"Fetching trending topics from r/{subreddit}")
        
        # Mock trending topics
        return [
            {
                "topic": "AI in Product Management",
                "mentions": 45,
                "growth": "+120%",
                "sentiment": "very positive"
            },
            {
                "topic": "Product-Led Growth",
                "mentions": 38,
                "growth": "+85%",
                "sentiment": "positive"
            },
            {
                "topic": "Remote PM Teams",
                "mentions": 32,
                "growth": "+45%",
                "sentiment": "neutral"
            },
            {
                "topic": "Automation Tools",
                "mentions": 28,
                "growth": "+95%",
                "sentiment": "positive"
            }
        ]
    
    async def monitor_brand_mentions(
        self,
        brand_name: str,
        subreddits: List[str]
    ) -> Dict[str, Any]:
        """Monitor mentions of a brand across subreddits"""
        logger.info(f"Monitoring mentions of '{brand_name}' across {len(subreddits)} subreddits")
        
        # Mock brand monitoring
        return {
            "brand": brand_name,
            "subreddits_monitored": subreddits,
            "total_mentions": 12,
            "sentiment": "positive",
            "mentions": [
                {
                    "subreddit": "ProductManagement",
                    "post_title": f"Has anyone tried {brand_name}?",
                    "score": 23,
                    "sentiment": "curious",
                    "url": "https://reddit.com/r/ProductManagement/comments/xyz"
                },
                {
                    "subreddit": "SaaS",
                    "post_title": f"Review: {brand_name} for PM workflows",
                    "score": 45,
                    "sentiment": "positive",
                    "url": "https://reddit.com/r/SaaS/comments/abc"
                }
            ]
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check Reddit API health"""
        return {
            "connected": self.connected,
            "status": "mock" if not self.connected else "connected"
        }


# Global instance
reddit_api = RedditAPI()

