#!/usr/bin/env python3
"""
Script to ingest the entire Physical AI & Humanoid Robotics textbook into the vector database.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the api directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "physical-ai-textbook" / "api"))

from services.rag_service import RAGService
from services.vector_db_service import VectorDBService
from services.document_ingestion_service import DocumentIngestionService

async def main():
    print("Starting textbook ingestion process...")
    
    # Initialize services
    rag_service = RAGService()
    vector_db_service = VectorDBService()
    ingestion_service = DocumentIngestionService(rag_service, vector_db_service)
    
    # Path to the textbook content
    textbook_path = Path(__file__).parent.parent / "physical-ai-textbook" / "docs"
    
    if not textbook_path.exists():
        print(f"Error: Textbook path does not exist: {textbook_path}")
        sys.exit(1)
    
    print(f"Ingesting textbook content from: {textbook_path}")
    
    # Process and ingest the entire textbook
    success = await ingestion_service.process_and_ingest_book()
    
    if success:
        print("✅ Textbook ingestion completed successfully!")
        
        # Show collection info
        info = await vector_db_service.get_collection_info()
        print(f"📊 Collection info: {info}")
    else:
        print("❌ Textbook ingestion failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())