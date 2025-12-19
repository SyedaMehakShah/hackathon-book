from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost/dbname"

    # Qdrant settings
    QDRANT_URL: str = "https://your-cluster-url.qdrant.io"
    QDRANT_API_KEY: Optional[str] = None

    # Cohere settings
    COHERE_API_KEY: str = ""
    
    # Application settings
    APP_NAME: str = "Integrated RAG Chatbot"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # RAG-specific settings
    CHUNK_SIZE: int = 400  # tokens
    CHUNK_OVERLAP: int = 75  # tokens
    TOP_K: int = 5
    MIN_SIMILARITY_THRESHOLD: float = 0.5
    MAX_CONTEXT_WINDOW: int = 3000  # tokens
    
    # Performance settings
    RESPONSE_TIMEOUT: int = 25  # seconds (ensures <= 2.5s avg)
    
    class Config:
        env_file = ".env"

settings = Settings()