from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # --- LLM Configuration --- 
    gemini_api: str
    
    # --- App Configuration --- 
    debug: bool = True
    app_name: str = "Notion-MCP-Chat"
    log_level: str = "INFO"
    
    # --- MCP Configuration --- 
    mcp_config_path: str = "app/mcp/config/mcp_config.json"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# --- Create settings instance ---
settings = Settings()
