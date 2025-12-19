import asyncio
import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from services.rag_service import RAGService
from services.vector_db_service import VectorDBService

async def main():
    print("Checking vector database status...")
    
    # Initialize services
    rag_service = RAGService()
    vector_db_service = VectorDBService()
    
    # Check collection info
    try:
        collection_info = await vector_db_service.get_collection_info()
        print(f"Collection info: {collection_info}")
        
        if collection_info and 'point_count' in collection_info:
            print(f"Number of documents in database: {collection_info['point_count']}")
            if collection_info['point_count'] > 0:
                print("✅ Database has documents - ingestion was successful!")
            else:
                print("❌ Database is empty - ingestion is needed")
        else:
            print("⚠️ Could not retrieve document count")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        print("This might indicate an issue with the Qdrant connection")
    
    # Try a basic search to see if it works
    try:
        results = await rag_service.search_documents("test", top_k=1)
        print(f"Search test results: {len(results)} results found")
        if results:
            print(f"First result sample: {results[0].get('content', '')[:100]}...")
    except Exception as e:
        print(f"❌ Error during search test: {e}")

if __name__ == "__main__":
    asyncio.run(main())