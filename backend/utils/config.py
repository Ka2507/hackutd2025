"""
Configuration management for ProdPlex backend.

Handles environment variables and settings using Pydantic.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    app_name: str = "ProdPlex"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    def get_port(self) -> int:
        """Get port from PORT environment variable (for production) or default."""
        return int(os.getenv("PORT", self.api_port))
    
    # CORS Settings
    # Can be set via CORS_ORIGINS env var as comma-separated string
    # Default includes localhost for development
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    def get_cors_origins(self) -> list:
        """Get CORS origins from environment variable or default."""
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            # Split by comma and strip whitespace
            return [origin.strip() for origin in cors_env.split(",")]
        return self.cors_origins
    
    # AI Model Settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3:8b"
    
    # NVIDIA Nemotron Settings
    nemotron_api_key: Optional[str] = None
    nemotron_base_url: str = "https://integrate.api.nvidia.com/v1"
    nemotron_model: str = "nvidia/nemotron-4-340b-instruct"
    nemotron_max_calls: int = 100
    
    # Budget Settings
    total_budget: float = 60.0
    budget_warning_threshold: float = 50.0
    
    # Vector Store Settings
    vector_store_type: str = "faiss"
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "prodigypm"
    
    # Integration API Keys
    jira_api_token: Optional[str] = None
    jira_base_url: Optional[str] = None
    slack_bot_token: Optional[str] = None
    figma_access_token: Optional[str] = None
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    
    # Database Settings
    context_db_path: str = "db/context.db"
    
    # Agent Settings
    max_agent_iterations: int = 5
    agent_timeout: int = 300
    
    class Config:
        """Pydantic configuration."""
        
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


settings = Settings()
