from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Physical AI & Humanoid Robotics Textbook API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("APP_ENV", "development")
    
    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = int(os.getenv("PORT", 8000))
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # Qdrant settings
    qdrant_host: str = os.getenv("QDRANT_HOST", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")
    
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Auth settings
    auth_secret: str = os.getenv("AUTH_SECRET", "")
    auth_url: str = os.getenv("AUTH_URL", "http://localhost:3000")
    
    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    
    class Config:
        env_file = ".env"

# Create a single instance of settings
settings = Settings()

def get_settings():
    return settings