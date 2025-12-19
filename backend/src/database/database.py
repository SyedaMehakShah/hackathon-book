import os
import logging
from functools import lru_cache
from typing import AsyncGenerator
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.rag_service import RAGService
from src.utils.config import settings

# Load environment variables explicitly to ensure .env values override system values
load_dotenv(override=True)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Postgres database setup
DATABASE_URL = settings.DATABASE_URL
async_engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    async_session_class=AsyncSession,
    bind=async_engine,
    expire_on_commit=False
)

# Qdrant vector database setup with fallback to in-memory if remote connection fails
try:
    qdrant_client = AsyncQdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        timeout=30,  # 30 seconds timeout
    )
    # Test the connection
    import asyncio
    async def test_connection():
        await qdrant_client.get_collections()
    asyncio.run(test_connection())
    logger.info("Connected to remote Qdrant instance")
except Exception as e:
    logger.warning(f"Could not connect to remote Qdrant: {e}. Using in-memory instance.")
    qdrant_client = AsyncQdrantClient(":memory:")
    logger.info("Initialized in-memory Qdrant client")

@lru_cache()
def get_rag_service():
    """Provide RAG service instance with database connections"""
    return RAGService(
        postgres_session=AsyncSessionLocal,
        qdrant_client=qdrant_client,
        cohere_api_key=settings.COHERE_API_KEY
    )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        yield session