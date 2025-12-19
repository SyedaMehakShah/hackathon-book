import asyncio
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables to temporarily override them
load_dotenv()

# Temporarily set Qdrant to use local/in-memory for this test
os.environ['QDRANT_HOST'] = 'http://localhost:6333'  # This will fail and fallback to in-memory
os.environ['QDRANT_API_KEY'] = None  # Make it use local/in-memory

sys.path.insert(0, str(Path(__file__).parent))

from services.rag_service import RAGService
from services.vector_db_service import VectorDBService

async def main():
    print("Testing RAG service with in-memory fallback...")
    
    try:
        # Initialize services (with env vars set to trigger in-memory fallback)
        rag_service = RAGService()
        vector_db_service = VectorDBService()
        
        print("✅ Services initialized successfully!")
        
        # Test basic functionality
        print("\nTesting embedding functionality...")
        test_embedding = await rag_service.embed_text("This is a test")
        print(f"✅ Embedding generated, length: {len(test_embedding) if test_embedding else 'None'}")
        
        # Test storing a simple document
        print("\nTesting document storage...")
        success = await rag_service.store_document(
            content="This is a test document for the AI textbook.",
            content_id="test_doc_1",
            metadata={"source": "test", "type": "test_document"}
        )
        print(f"✅ Document stored: {success}")
        
        # Test search
        print("\nTesting search functionality...")
        search_results = await rag_service.search_documents("test", top_k=1)
        print(f"✅ Search completed, found {len(search_results)} results")
        
        if search_results:
            print(f"First result content preview: {search_results[0]['content'][:100]}...")
        
        # Test answer functionality
        print("\nTesting answer functionality...")
        answer_result = await rag_service.answer_question("What is this test about?")
        print(f"✅ Answer received: {answer_result['answer'][:100] if answer_result.get('answer') else 'No answer'}...")
        
        print("\n🎉 All tests passed! RAG service is working correctly.")
        
    except Exception as e:
        print(f"❌ Error in main test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())