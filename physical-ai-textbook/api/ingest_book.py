import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from services.rag_service import RAGService
from services.vector_db_service import VectorDBService
from services.document_ingestion_service import DocumentIngestionService

async def main():
    print("Starting textbook ingestion process...")

    # Initialize services
    print("Initializing services...")
    rag_service = RAGService()
    vector_db_service = VectorDBService()
    ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

    print("Services initialized. Starting to process and ingest textbook...")

    # Process and ingest the entire book
    success = await ingestion_service.process_and_ingest_book()

    if success:
        print("✅ Successfully ingested the entire textbook into the vector database!")
        print("The RAG system now has access to the textbook content.")
    else:
        print("❌ Failed to ingest the textbook.")

    # Check collection info to confirm data was ingested
    try:
        collection_info = await vector_db_service.get_collection_info()
        if collection_info:
            print(f"📚 Collection info: {collection_info}")
        else:
            print("⚠️ Could not retrieve collection info")
    except Exception as e:
        print(f"⚠️ Error retrieving collection info: {e}")

    # Close the services if they have a close method
    try:
        if hasattr(rag_service, 'close'):
            await rag_service.close()
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())