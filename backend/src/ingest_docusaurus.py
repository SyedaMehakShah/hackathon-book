import asyncio
import json
import sys
import os
import argparse
from pathlib import Path

# Add the backend directory to the path so we can import our modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from src.services.rag_service import RAGService
from src.database.database import get_rag_service
from src.utils.text_processor import chunk_text
from src.utils.doc_extractor import traverse_docs_directory, clean_markdown_content

async def ingest_docusaurus_content(dry_run=False):
    """
    Ingest Docusaurus documentation content into the RAG system
    """
    print(f"Starting Docusaurus content ingestion... (Dry run: {dry_run})")

    # Get the RAG service instance
    rag_service = get_rag_service()

    # Initialize the Qdrant collection if it doesn't exist
    if not dry_run:
        print("Initializing Qdrant collection...")
        await rag_service.initialize_qdrant_collection()

    # Define the path to the docs directory
    docs_path = "../physical-ai-textbook/docs"

    if not os.path.exists(docs_path):
        print(f"Docs directory not found at {docs_path}")
        return

    # Extract all documents
    documents = traverse_docs_directory(docs_path)

    print(f"Found {len(documents)} markdown documents to process")

    # Process each document
    total_chunks = 0
    for i, doc in enumerate(documents):
        print(f"Processing document {i+1}/{len(documents)}: {doc['relative_path']}")

        # Clean the content
        cleaned_content = clean_markdown_content(doc['content'])

        # Extract metadata
        book_id = "physical-ai-textbook"  # As specified in the requirements
        chapter = doc['chapter']
        page_name = doc['page_name']

        # If in dry run mode, skip actual indexing but simulate the process
        if dry_run:
            # Simulate chunking without actually storing
            chunked_data = chunk_text(
                cleaned_content,
                400,  # Using default chunk size
                75,   # Using default overlap
                book_id=book_id,
                chapter=chapter,
                page_number=i+1
            )

            simulated_result = {
                "document_title": page_name,
                "status": "simulated",
                "chunks_indexed": len(chunked_data)
            }

            print(f"  - Would index {simulated_result['chunks_indexed']} chunks to Qdrant (dry run)")
            print(f"    Sample chunk: {chunked_data[0]['content'][:100]}..." if chunked_data else "")
        else:
            try:
                # Process and index each document
                result = await rag_service.index_document(
                    book_id=book_id,
                    content=cleaned_content,
                    title=page_name,
                    chapter=chapter,
                    page_number=i+1,
                    source_file=doc['relative_path']
                )

                total_chunks += result["chunks_indexed"]
                print(f"  - Indexed {result['chunks_indexed']} chunks to Qdrant")
            except Exception as e:
                print(f"  - Error indexing document {doc['relative_path']}: {str(e)}")
                print("  Please verify your API keys and connection settings in the .env file")
                print("  Required settings: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY")
                continue  # Continue with the next document

    if dry_run:
        print("Dry run completed! No data was written to Qdrant.")
    else:
        print(f"Ingestion completed! Total chunks indexed: {total_chunks}")
        print("Docusaurus content is now available in the RAG system.")

async def main():
    parser = argparse.ArgumentParser(description='Ingest Docusaurus documentation content')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the ingestion without writing to Qdrant')

    args = parser.parse_args()

    await ingest_docusaurus_content(dry_run=args.dry_run)

if __name__ == "__main__":
    asyncio.run(main())