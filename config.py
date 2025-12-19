"""
Lightweight configuration loader that avoids external dependency on
`pydantic-settings`. Reads environment variables (via .env) and exposes
a `settings` instance similar to the original implementation.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


class Settings:
    def __init__(self):
        # AI Model Configuration
        self.use_llm = os.getenv("USE_LLM", "false").lower() == "true"
        self.ai_provider = os.getenv("AI_PROVIDER", "openai")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.model_temperature = float(os.getenv("MODEL_TEMPERATURE", "0.3"))
        self.model_name_openai = os.getenv("MODEL_NAME_OPENAI", "gpt-4-turbo-preview")
        self.model_name_gemini = os.getenv("MODEL_NAME_GEMINI", "gemini-pro")

        # Multilingual Configuration
        self.supported_languages = ["en", "hi", "te", "kn"]
        self.multilingual_embedding_model = os.getenv(
            "MULTILINGUAL_EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "en")

        # RAG Configuration
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./vector_db")
        self.top_k_results = int(os.getenv("TOP_K_RESULTS", "4"))

        # Data Paths
        self.data_folder = os.getenv("DATA_FOLDER", "./data")
        self.audio_folder = os.getenv("AUDIO_FOLDER", "./audio")
        self.transcripts_folder = os.getenv("TRANSCRIPTS_FOLDER", "./transcripts")

        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_reload = os.getenv("API_RELOAD", "false").lower() == "true"

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "app.log")

    def validate_config(self) -> None:
        # Only require API keys if LLM mode is explicitly enabled
        if self.use_llm:
            if self.ai_provider == "openai" and not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when use_llm=true and provider=openai")
            if self.ai_provider == "gemini" and not self.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required when use_llm=true and provider=gemini")

        # Ensure folders exist
        Path(self.data_folder).mkdir(parents=True, exist_ok=True)
        Path(self.audio_folder).mkdir(parents=True, exist_ok=True)
        Path(self.transcripts_folder).mkdir(parents=True, exist_ok=True)
        Path(self.vector_db_path).mkdir(parents=True, exist_ok=True)

    @property
    def model_name(self) -> str:
        return self.model_name_openai if self.ai_provider == "openai" else self.model_name_gemini


# Instantiate global settings
settings = Settings()
settings.validate_config()
