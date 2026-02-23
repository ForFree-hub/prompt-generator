"""
Configuration settings for Prompt Generator AI Agent
"""

import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AppConfig:
    """Application configuration class"""
    
    # Application Settings
    app_name: str = "PromptGen Pro"
    app_version: str = "1.0.0"
    debug_mode: bool = False
    
    # API Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # UI Settings
    theme: str = "dark"
    sidebar_state: str = "expanded"
    
    # History Settings
    max_history_items: int = 50
    history_file: str = "data/history.json"
    favorites_file: str = "data/favorites.json"
    
    # Prompt Engineering Settings
    default_complexity: str = "Professional"
    default_tone: str = "Professional"
    default_length: str = "Detailed"
    
    # Output Settings
    supported_formats: List[str] = None
    
    def __post_init__(self):
        self.supported_formats = ["Markdown", "JSON", "XML", "Plain Text", "Code Block"]
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            debug_mode=os.getenv("DEBUG_MODE", "False").lower() == "true"
        )


# Global config instance
Config = AppConfig()