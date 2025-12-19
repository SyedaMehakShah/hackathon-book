import asyncio
import sys
from pathlib import Path
import logging
import gc
import psutil  # For monitoring memory usage
import os
from typing import List, Dict, Any

# Add the backend directory to the path so we can import our modules
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Explicitly load environment variables at the start
from dotenv import load_dotenv
load_dotenv(override=True)

from src.database.database import get_rag_service

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / 1024 / 1024  # Convert to MB

async def process_query_batch(queries: List[Dict[str, Any]], rag_service) -> List[Dict[str, Any]]:
    """
    Process a batch of queries efficiently, limiting concurrent operations to manage memory.
    """
    results = []
    
    # Process queries one at a time to minimize memory usage
    for i, query_data in enumerate(queries):
        logger.info(f"Processing query {i+1}/{len(queries)}")
        
        try:
            # Get memory before processing
            mem_before = get_memory_usage()
            
            # Process the query based on type
            if query_data['type'] == 'global':
                result = await rag_service.query_global(
                    question=query_data['question'],
                    book_id=query_data['book_id'],
                    session_id=query_data.get('session_id')
                )
            elif query_data['type'] == 'selected_text':
                result = await rag_service.query_selected_text(
                    question=query_data['question'],
                    selected_text=query_data['selected_text'],
                    session_id=query_data.get('session_id')
                )
            else:
                raise ValueError(f"Unknown query type: {query_data['type']}")
            
            results.append({
                'query_id': query_data.get('query_id', i),
                'result': result,
                'success': True
            })
            
            # Free memory after processing each query
            gc.collect()
            
            # Get memory after processing
            mem_after = get_memory_usage()
            logger.info(f"Query {i+1} processed. Memory change: {mem_after - mem_before:.2f} MB")
            
        except Exception as e:
            logger.error(f"Error processing query {i+1}: {str(e)}")
            results.append({
                'query_id': query_data.get('query_id', i),
                'error': str(e),
                'success': False
            })
            
            # Still perform garbage collection even if there was an error
            gc.collect()
    
    return results

async def main():
    initial_memory = get_memory_usage()
    logger.info(f"Initial memory usage: {initial_memory:.2f} MB")
    
    logger.info("Loading RAG service with fresh environment...")

    try:
        # Get the RAG service instance (this should now use the correct env values)
        rag_service = get_rag_service()

        # Display what URL the client is using
        logger.info(f"Qdrant client URL: {rag_service.qdrant_client._client._host}")

        logger.info("Preparing to process batch queries...")

        # Example batch of queries to process
        # In a real implementation, these would come from an API request, file, or database
        queries_to_process = [
            {
                'query_id': 1,
                'type': 'global',
                'question': 'What is embodied intelligence?',
                'book_id': 'physical-ai-textbook',
                'session_id': 'session_1'
            },
            {
                'query_id': 2,
                'type': 'global',
                'question': 'How does ROS 2 work?',
                'book_id': 'physical-ai-textbook',
                'session_id': 'session_1'
            }
            # Add more queries here as needed
        ]

        logger.info(f"Processing {len(queries_to_process)} queries in batch...")

        # Process queries in the batch
        results = await process_query_batch(queries_to_process, rag_service)

        # Report results
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        logger.info(f"Batch processing completed!")
        logger.info(f"Successful queries: {successful}")
        logger.info(f"Failed queries: {failed}")

        final_memory = get_memory_usage()
        logger.info(f"Final memory usage: {final_memory:.2f} MB")
        logger.info(f"Memory change during run: {final_memory - initial_memory:.2f} MB")

    except Exception as e:
        logger.error(f"Error during batch processing: {str(e)}")
        import traceback
        logger.error(f"Full error trace: {traceback.format_exc()}")
        sys.exit(1)
    finally:
        # Ensure cleanup of resources
        try:
            await rag_service.close()
        except:
            pass  # Ignore cleanup errors

if __name__ == "__main__":
    asyncio.run(main())