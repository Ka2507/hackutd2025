"""
Configuration management for ProdigyPM backend.

Handles environment variables and settings using Pydantic.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    app_name: str = "ProdigyPM"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS Settings
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # AI Model Settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3:8b"
    
    # NVIDIA Nemotron Settings
    nemotron_api_key: Optional[str] = None
    nemotron_base_url: str = "https://integrate.api.nvidia.com/v1"
    nemotron_model: str = "nvidia/nemotron-4-340b-instruct"
    nemotron_max_calls: int = 3
    
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


settings = Settings()
