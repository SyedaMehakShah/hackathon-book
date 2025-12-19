"""
Application initializer to set up the RAG service with proper configuration
"""
import asyncio
from src.database.database import get_rag_service
from src.utils.config import settings

async def initialize_app():
    """
    Initialize the application by setting up required services
    """
    # Get the RAG service instance
    rag_service = get_rag_service()
    
    # Initialize the Qdrant collection
    await rag_service.initialize_qdrant_collection()
    
    print("Application initialized successfully")
    print(f"Qdrant collection '{rag_service.collection_name}' is ready")
    print(f"Using Cohere embeddings model: embed-multilingual-v3.0")
    print(f"Using Cohere generation model: command-r")

if __name__ == "__main__":
    asyncio.run(initialize_app())