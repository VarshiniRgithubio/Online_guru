"""
Configuration management for the Sai Baba Guidance Chatbot.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AI Model Configuration
    ai_provider: Literal["openai", "gemini"] = "openai"
    openai_api_key: str = ""
    google_api_key: str = ""
    model_temperature: float = 0.3
    model_name_openai: str = "gpt-4-turbo-preview"
    model_name_gemini: str = "gemini-pro"
    
    # Multilingual Configuration
    supported_languages: list = ["en", "hi", "te", "kn"]
    multilingual_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_language: str = "en"
    
    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    vector_db_path: str = "./vector_db"
    top_k_results: int = 4
    
    # Data Paths
    data_folder: str = "./data"
    audio_folder: str = "./audio"
    transcripts_folder: str = "./transcripts"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def validate_config(self) -> None:
        """Validate configuration and create necessary directories."""
        # Check API keys
        if self.ai_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        if self.ai_provider == "gemini" and not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required when using Gemini provider")
        
        # Create directories if they don't exist
        Path(self.data_folder).mkdir(parents=True, exist_ok=True)
        Path(self.audio_folder).mkdir(parents=True, exist_ok=True)
        Path(self.transcripts_folder).mkdir(parents=True, exist_ok=True)
        Path(self.vector_db_path).mkdir(parents=True, exist_ok=True)
    
    @property
    def model_name(self) -> str:
        """Get the appropriate model name based on provider."""
        return self.model_name_openai if self.ai_provider == "openai" else self.model_name_gemini


# Global settings instance
settings = Settings()
