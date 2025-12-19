import asyncio
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentIngestionService:
    def __init__(self, rag_service, vector_db_service):
        self.rag_service = rag_service
        self.vector_db_service = vector_db_service

    async def ingest_from_directory(self, directory_path: str) -> bool:
        """
        Ingest all markdown documents from a directory
        """
        try:
            directory = Path(directory_path)
            if not directory.exists():
                logger.error(f"Directory does not exist: {directory_path}")
                return False

            # Get all markdown files
            markdown_files = list(directory.rglob("*.md"))
            logger.info(f"Found {len(markdown_files)} markdown files to ingest")

            success_count = 0
            for file_path in markdown_files:
                if await self.ingest_document(str(file_path)):
                    success_count += 1

            logger.info(f"Successfully ingested {success_count}/{len(markdown_files)} documents")
            return success_count == len(markdown_files)
        except Exception as e:
            logger.error(f"Error ingesting from directory: {e}")
            return False

    async def ingest_document(self, file_path: str) -> bool:
        """
        Ingest a single document from a file path
        """
        try:
            # Read the document content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Create a document ID from the file path
            doc_id = self._generate_doc_id(file_path)

            # Store the document in the vector database
            success = await self.rag_service.store_document(
                content=content,
                content_id=doc_id,
                metadata={"source_file": file_path, "type": "textbook_chapter"}
            )

            if success:
                logger.info(f"Successfully ingested document: {file_path}")
            else:
                logger.error(f"Failed to ingest document: {file_path}")

            return success
        except Exception as e:
            logger.error(f"Error ingesting document {file_path}: {e}")
            return False

    async def ingest_text_chunks(self, text_chunks: List[Dict[str, str]], source: str = "manual") -> bool:
        """
        Ingest a list of text chunks with their IDs and metadata
        """
        try:
            success_count = 0
            for chunk in text_chunks:
                chunk_text = chunk.get("text", "")
                chunk_id = chunk.get("id", "")
                metadata = chunk.get("metadata", {})

                if not chunk_id:
                    # Generate an ID if not provided
                    chunk_id = self._generate_doc_id(f"{source}_{len(chunk_text)}")

                success = await self.rag_service.store_document(
                    content=chunk_text,
                    content_id=chunk_id,
                    metadata={**metadata, "source": source}
                )

                if success:
                    success_count += 1

            logger.info(f"Successfully ingested {success_count}/{len(text_chunks)} text chunks")
            return success_count == len(text_chunks)
        except Exception as e:
            logger.error(f"Error ingesting text chunks: {e}")
            return False

    async def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, str]]:
        """
        Chunk text into smaller pieces with overlap
        """
        try:
            chunks = []
            start = 0
            text_length = len(text)

            while start < text_length:
                end = start + chunk_size

                # If we're near the end, take the remaining text
                if end > text_length:
                    end = text_length

                chunk = text[start:end]
                chunks.append({
                    "text": chunk,
                    "id": self._generate_doc_id(f"chunk_{start}_{end}"),
                })

                # Move start position by chunk_size - overlap
                start = end - overlap

            logger.info(f"Chunked text into {len(chunks)} pieces")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return []

    def _generate_doc_id(self, source: str) -> str:
        """
        Generate a document ID based on the source
        """
        import hashlib
        import time
        # Create a unique ID based on the source and timestamp
        unique_str = f"{source}_{time.time()}"
        return hashlib.md5(unique_str.encode()).hexdigest()

    async def process_and_ingest_book(self) -> bool:
        """
        Process and ingest the entire textbook from the docs directory
        """
        try:
            docs_path = "C:/Users/Admin/hackathon/physical-ai-textbook/docs"
            if not os.path.exists(docs_path):
                logger.error(f"Docs directory does not exist: {docs_path}")
                return False

            logger.info("Starting to process and ingest the entire textbook...")
            success = await self.ingest_from_directory(docs_path)
            
            if success:
                logger.info("Successfully ingested the entire textbook into the vector database")
            else:
                logger.error("Failed to ingest the textbook")
            
            return success
        except Exception as e:
            logger.error(f"Error processing and ingesting textbook: {e}")
            return False