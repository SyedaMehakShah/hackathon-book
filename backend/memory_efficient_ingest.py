import asyncio
import sys
import gc
from pathlib import Path
import logging
import os
from typing import AsyncGenerator, Dict, Any
import psutil  # For monitoring memory usage

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

def should_exclude_path(file_path: str) -> bool:
    """
    Determine if a file or directory should be excluded from processing.
    """
    exclusions = [
        '.git',
        '__pycache__',
        '.DS_Store',
        'Thumbs.db',
        '.env',
        '.venv',
        '.next',
        'dist',
        'build',
        '*.log',
        '*.tmp',
        '*.bak',
        'coverage',
        '.pytest_cache',
        '.vscode',
        '.idea',
        # Add any other directories or files you don't want to process
    ]
    
    path_obj = Path(file_path)
    
    # Check if it's an exclusion pattern
    for exclusion in exclusions:
        if exclusion.startswith('*'):  # Wildcard pattern
            if path_obj.match(exclusion):
                return True
        elif exclusion in str(path_obj):  # Contains pattern
            return True
    
    return False

def process_single_document(file_path: str, docs_path: str) -> Dict[str, Any]:
    """
    Process a single document and return its record.
    This function loads minimal data to avoid memory issues.
    """
    from src.utils.doc_extractor import extract_text_from_markdown, get_chapter_info_from_path, get_page_name_from_path
    
    # Extract content and metadata
    content, frontmatter_meta = extract_text_from_markdown(file_path)

    # Get chapter information based on path
    chapter = get_chapter_info_from_path(file_path, {})

    # Get page name
    page_name = get_page_name_from_path(file_path)

    # Create document record
    doc_record = {
        'file_path': file_path,
        'relative_path': os.path.relpath(file_path, docs_path),
        'content': content,
        'frontmatter': frontmatter_meta,
        'chapter': chapter,
        'page_name': page_name,
        'file_name': Path(file_path).name
    }
    
    return doc_record

async def process_documents_batched(docs_path: str, batch_size: int = 5) -> AsyncGenerator[list, None]:
    """
    Process documents in batches to minimize memory usage.
    Yields one batch at a time instead of loading all documents.
    """
    import os
    from src.utils.doc_extractor import clean_markdown_content
    
    batch = []
    
    for root, dirs, files in os.walk(docs_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.join(root, d))]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Skip excluded files
                if should_exclude_path(file_path):
                    continue
                
                try:
                    # Process the document and get its record
                    doc_record = process_single_document(file_path, docs_path)
                    
                    batch.append(doc_record)
                    
                    # Yield batch when it reaches the specified size
                    if len(batch) >= batch_size:
                        yield batch
                        # Clear the batch to free memory
                        batch = []
                        
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    continue
    
    # Yield remaining documents if any
    if batch:
        yield batch

async def main():
    initial_memory = get_memory_usage()
    logger.info(f"Initial memory usage: {initial_memory:.2f} MB")

    logger.info("Loading RAG service with fresh environment...")

    try:
        # Get the RAG service instance
        rag_service = get_rag_service()

        # Display what URL the client is using
        logger.info(f"Qdrant client URL: {rag_service.qdrant_client._client._host}")

        # Initialize the Qdrant collection if it doesn't exist
        logger.info("Initializing Qdrant collection...")
        await rag_service.initialize_qdrant_collection()
        logger.info("Qdrant collection initialized successfully!")

        logger.info("Now proceeding with document ingestion...")

        # Define the path to the docs directory
        docs_path = "../physical-ai-textbook/docs"

        # Resolve the path relative to the backend directory
        docs_full_path = Path(backend_dir / docs_path).resolve()
        logger.info(f"Looking for docs at: {docs_full_path}")

        if not docs_full_path.exists():
            logger.error(f"Docs directory not found at {docs_full_path}")
            # Try alternative path relative to current working directory
            alt_docs_path = Path("../physical-ai-textbook/docs").resolve()
            if alt_docs_path.exists():
                docs_path = str(alt_docs_path)
                logger.info(f"Using alternative path: {docs_path}")
            else:
                logger.error(f"Docs directory not found at {alt_docs_path} either")
                return

        # Process documents in batches to manage memory efficiently
        batch_size = 5  # Small batch size to keep memory usage low
        total_chunks = 0
        successful_docs = 0
        failed_docs = 0
        total_processed = 0

        logger.info(f"Starting batched document processing with batch size: {batch_size}")

        # Process documents in batches
        batch_num = 0
        async for batch in process_documents_batched(str(docs_path), batch_size):
            batch_num += 1
            batch_memory_before = get_memory_usage()
            logger.info(f"Processing batch {batch_num} with {len(batch)} documents")
            logger.info(f"Memory usage before batch: {batch_memory_before:.2f} MB")

            # Process each document in the batch
            for i, doc in enumerate(batch):
                total_processed += 1
                logger.info(f"Processing document {total_processed}: {doc['relative_path']}")

                try:
                    # Clean the content (only here, to minimize memory holding)
                    from src.utils.doc_extractor import clean_markdown_content
                    cleaned_content = clean_markdown_content(doc['content'])

                    # Extract metadata
                    book_id = "physical-ai-textbook"  # As specified in the requirements
                    chapter = doc['chapter']
                    page_name = doc['page_name']

                    # Process and index each document
                    result = await rag_service.index_document(
                        book_id=book_id,
                        content=cleaned_content,
                        title=page_name,
                        chapter=chapter,
                        page_number=total_processed,
                        source_file=doc['relative_path']
                    )

                    total_chunks += result["chunks_indexed"]
                    successful_docs += 1
                    logger.info(f"  - Indexed {result['chunks_indexed']} chunks to Qdrant")

                    # Explicitly delete large variables to free memory immediately
                    del cleaned_content

                except Exception as e:
                    logger.error(f"  - Error indexing document {doc['relative_path']}: {str(e)}")
                    import traceback
                    logger.error(f"  - Full error trace: {traceback.format_exc()}")
                    failed_docs += 1
                    continue  # Continue with the next document

                # Explicitly delete the document data to free memory
                del doc

            # Force garbage collection between batches to free memory
            gc.collect()

            batch_memory_after = get_memory_usage()
            logger.info(f"Memory usage after batch: {batch_memory_after:.2f} MB")
            logger.info(f"Memory difference for batch: {batch_memory_after - batch_memory_before:.2f} MB")

            logger.info(f"Completed batch {batch_num}, processed {total_processed} documents in total...")

            # Optional: Add small delay between batches to allow system to catch up
            await asyncio.sleep(0.1)

        final_memory = get_memory_usage()
        logger.info(f"Final memory usage: {final_memory:.2f} MB")
        logger.info(f"Memory change during run: {final_memory - initial_memory:.2f} MB")

        logger.info(f"Ingestion completed!")
        logger.info(f"Total documents processed: {total_processed}")
        logger.info(f"Total chunks indexed: {total_chunks}")
        logger.info(f"Documents processed successfully: {successful_docs}")
        logger.info(f"Documents failed: {failed_docs}")
        logger.info("Docusaurus content is now available in the RAG system.")

    except Exception as e:
        logger.error(f"Error during ingestion process: {str(e)}")
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