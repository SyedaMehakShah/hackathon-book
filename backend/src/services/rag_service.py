import asyncio
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from sqlalchemy.ext.asyncio import AsyncSession
import cohere  # Using Cohere as required by constitution
from src.models.chunk import Chunk
from src.models.book import Book
from src.utils.config import settings
from src.utils.text_processor import chunk_text, embed_text, embed_texts

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, postgres_session: AsyncSession, qdrant_client: AsyncQdrantClient, cohere_api_key: str):
        self.postgres_session = postgres_session
        self.qdrant_client = qdrant_client
        self.cohere_client = cohere.AsyncClient(cohere_api_key)
        self.collection_name = "book_chunks"

    async def initialize_qdrant_collection(self):
        """Initialize the Qdrant collection for storing book chunks"""
        try:
            # Check if collection exists
            collections = await self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with appropriate vector configuration
                await self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # Cohere embed-multilingual-v3.0 returns 1024-dim vectors
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload index for book_id to optimize searches
                await self.qdrant_client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="book_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                # Create payload index for chapter to optimize searches
                await self.qdrant_client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chapter",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    async def index_book(self, book_id: str, title: str, author: str, content: str, chapter: str = None, page_number: int = None) -> Dict[str, Any]:
        """Index a book by chunking its content and storing in vector database"""
        import httpx
        import asyncio
        from qdrant_client.http.exceptions import ResponseHandlingException

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                logger.info(f"Starting to index book: {book_id} (attempt {attempt + 1})")

                # Chunk the content following constitutional requirements (300-500 tokens with 50-100 overlap)
                chunked_data = chunk_text(
                    content,
                    settings.CHUNK_SIZE,
                    settings.CHUNK_OVERLAP,
                    book_id=book_id,
                    chapter=chapter,
                    page_number=page_number
                )

                # Extract just the content for embedding
                chunk_contents = [chunk['content'] for chunk in chunked_data]

                # Create embeddings using Cohere in batch (as required by constitution)
                try:
                    embeddings = await embed_texts(chunk_contents, self.cohere_client, batch_size=20)
                except Exception as e:
                    logger.error(f"Failed to create embeddings: {e}")
                    raise

                # Prepare points for Qdrant
                points = []
                for i, (chunk_info, embedding) in enumerate(zip(chunked_data, embeddings)):
                    # Create point with metadata
                    point = models.PointStruct(
                        id=chunk_info['chunk_id'],
                        vector=embedding,
                        payload={
                            "book_id": chunk_info['book_id'],
                            "chunk_id": chunk_info['chunk_id'],
                            "content": chunk_info['content'],
                            "chapter": chunk_info['chapter'],
                            "page_number": chunk_info['page_number'],
                            "position": chunk_info['position']
                        }
                    )
                    points.append(point)

                # Upsert all points to Qdrant with error handling
                if points:
                    try:
                        await self.qdrant_client.upsert(
                            collection_name=self.collection_name,
                            points=points
                        )
                    except (httpx.TimeoutException, httpx.ConnectTimeout, ResponseHandlingException) as e:
                        logger.warning(f"Network error during upsert (attempt {attempt + 1}): {e}")
                        if attempt < max_retries - 1:  # Not the last attempt
                            logger.info(f"Retrying in {retry_delay} seconds...")
                            await asyncio.sleep(retry_delay)
                            continue  # Try again
                        else:
                            logger.error(f"Failed to upsert points to Qdrant after {max_retries} attempts: {e}")
                            logger.error("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
                            raise
                    except Exception as e:
                        logger.error(f"Failed to upsert points to Qdrant: {e}")
                        logger.error("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
                        raise

                logger.info(f"Successfully indexed book {book_id} with {len(points)} chunks")

                return {
                    "book_id": book_id,
                    "status": "completed",
                    "chunks_indexed": len(points)
                }
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Error indexing book {book_id} after {max_retries} attempts: {e}")
                    raise
                else:
                    logger.warning(f"Attempt {attempt + 1} failed for book {book_id}, retrying: {e}")
                    await asyncio.sleep(retry_delay)

        # This line should not be reached, but added for completeness
        raise Exception(f"Failed to index book after {max_retries} attempts")

    async def index_document(self, book_id: str, content: str, title: str = None, chapter: str = None, page_number: int = None, source_file: str = None) -> Dict[str, Any]:
        """Index a single document with detailed metadata"""
        import httpx
        import asyncio
        from qdrant_client.http.exceptions import ResponseHandlingException

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                logger.info(f"Starting to index document: {title or source_file} (attempt {attempt + 1})")

                # Chunk the content following constitutional requirements (300-500 tokens with 50-100 overlap)
                chunked_data = chunk_text(
                    content,
                    settings.CHUNK_SIZE,
                    settings.CHUNK_OVERLAP,
                    book_id=book_id,
                    chapter=chapter,
                    page_number=page_number
                )

                # Extract just the content for embedding
                chunk_contents = [chunk['content'] for chunk in chunked_data]

                # Create embeddings using Cohere in batch (as required by constitution)
                try:
                    embeddings = await embed_texts(chunk_contents, self.cohere_client, batch_size=20)
                except Exception as e:
                    logger.error(f"Failed to create embeddings: {e}")
                    raise

                # Prepare points for Qdrant
                points = []
                for i, (chunk_info, embedding) in enumerate(zip(chunked_data, embeddings)):
                    # Create point with detailed metadata
                    payload = {
                        "book_id": chunk_info['book_id'],
                        "chunk_id": chunk_info['chunk_id'],
                        "content": chunk_info['content'],
                        "chapter": chunk_info['chapter'],
                        "page_number": chunk_info['page_number'],
                        "position": chunk_info['position']
                    }

                    # Add optional metadata
                    if title:
                        payload["title"] = title
                    if source_file:
                        payload["source_file"] = source_file

                    point = models.PointStruct(
                        id=chunk_info['chunk_id'],
                        vector=embedding,
                        payload=payload
                    )
                    points.append(point)

                # Upsert all points to Qdrant with error handling
                if points:
                    try:
                        await self.qdrant_client.upsert(
                            collection_name=self.collection_name,
                            points=points
                        )
                    except (httpx.TimeoutException, httpx.ConnectTimeout, ResponseHandlingException) as e:
                        logger.warning(f"Network error during upsert (attempt {attempt + 1}): {e}")
                        if attempt < max_retries - 1:  # Not the last attempt
                            logger.info(f"Retrying in {retry_delay} seconds...")
                            await asyncio.sleep(retry_delay)
                            continue  # Try again
                        else:
                            logger.error(f"Failed to upsert points to Qdrant after {max_retries} attempts: {e}")
                            logger.error("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
                            raise
                    except Exception as e:
                        logger.error(f"Failed to upsert points to Qdrant: {e}")
                        logger.error("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
                        raise

                logger.info(f"Successfully indexed document '{title or source_file}' with {len(points)} chunks")

                return {
                    "document_title": title or source_file,
                    "status": "completed",
                    "chunks_indexed": len(points)
                }
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Error indexing document {title or source_file} after {max_retries} attempts: {e}")
                    raise
                else:
                    logger.warning(f"Attempt {attempt + 1} failed for document {title or source_file}, retrying: {e}")
                    await asyncio.sleep(retry_delay)

        # This line should not be reached, but added for completeness
        raise Exception(f"Failed to index document after {max_retries} attempts")

    async def query_global(self, question: str, book_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Query using global RAG mode - search entire book database"""
        try:
            # Generate embedding for the question using Cohere
            question_embedding = await embed_text(question, self.cohere_client)

            # Search in Qdrant for relevant chunks from the specified book
            try:
                search_result = await self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=question_embedding,
                    query_filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="book_id",
                                match=models.MatchValue(value=book_id)
                            )
                        ]
                    ),
                    limit=settings.TOP_K,
                    score_threshold=settings.MIN_SIMILARITY_THRESHOLD
                )
            except Exception as e:
                logger.error(f"Failed to search in Qdrant: {e}")
                logger.error("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
                raise

            # Extract relevant chunks and sources
            relevant_chunks = []
            sources = []

            for hit in search_result:
                if hit.score >= settings.MIN_SIMILARITY_THRESHOLD:
                    payload = hit.payload
                    chunk = Chunk(
                        chunk_id=payload.get("chunk_id", ""),
                        book_id=payload.get("book_id", ""),
                        content=payload.get("content", ""),
                        chapter=payload.get("chapter"),
                        page_number=payload.get("page_number"),
                        position=payload.get("position", 0)
                    )

                    relevant_chunks.append(chunk)
                    sources.append({
                        "chunk_id": payload.get("chunk_id", ""),
                        "chapter": payload.get("chapter"),
                        "page_number": payload.get("page_number"),
                        "text": payload.get("content", "")[:200] + "..."  # Truncate for display
                    })

            if not relevant_chunks:
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": []
                }

            # Construct context from relevant chunks
            context_parts = []
            for i, chunk in enumerate(relevant_chunks):
                part = f"Context {i+1} (Chapter: {chunk.chapter}, Page: {chunk.page_number}):\n{chunk.content}"
                context_parts.append(part)
            context = "\n\n".join(context_parts)

            # Generate answer using Cohere, ensuring it's grounded in the context
            prompt = f"""
            You are an AI assistant that answers questions based only on the provided context from a book.
            Answer the question using ONLY the information in the context.
            Do not use any external knowledge or make assumptions beyond what's in the context.
            If the answer is not available in the context, respond with exactly: "The selected content or book does not contain enough information to answer this question."

            Context:
            {context}

            Question: {question}

            Answer:
            """

            response = await self.cohere_client.generate(
                model='command-r',  # Using Cohere Command-R as required
                prompt=prompt,
                max_tokens=500,
                temperature=0.1,  # Lower temperature for more consistent, deterministic answers
                stop_sequences=["Question:", "Context:"]
            )

            answer = response.generations[0].text.strip()

            # Ensure the answer is grounded in the context by checking for the specific failure message
            if "does not contain enough information" in answer.lower():
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": []
                }

            # Perform basic validation to ensure the response is grounded in the context
            # If response is generic or seems to be hallucinated, return the failure message
            if self._is_response_fallback(answer):
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": []
                }

            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error in global query: {e}")
            raise

    async def query_selected_text(self, question: str, selected_text: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Query using only the selected text as context - NO global search"""
        try:
            # Validate that we have selected text
            if not selected_text or not selected_text.strip():
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": []
                }

            # Generate answer using only the selected text as context
            prompt = f"""
            You are an AI assistant that answers questions based only on the provided selected text.
            Answer the question using ONLY the information in the selected text.
            Do not use any external knowledge or information beyond what is provided in the selected text.
            Do NOT perform global vector search or access any other content.
            If the answer is not available in the selected text, respond with exactly: "The selected content or book does not contain enough information to answer this question."

            Selected Text:
            {selected_text}

            Question: {question}

            Answer:
            """

            response = await self.cohere_client.generate(
                model='command-r',  # Using Cohere Command-R as required
                prompt=prompt,
                max_tokens=500,
                temperature=0.1,  # Lower temperature for more consistent, deterministic answers
                stop_sequences=["Question:", "Selected Text:"]
            )

            answer = response.generations[0].text.strip()

            # Ensure the answer is grounded in the selected text
            if "does not contain enough information" in answer.lower():
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": [{"text": selected_text[:200] + "..."}]  # Include truncated text as source
                }

            # Perform basic validation to ensure the response is grounded in the selected text
            # If response is generic or seems to be hallucinated, return the failure message
            if self._is_response_fallback(answer):
                return {
                    "answer": "The selected content or book does not contain enough information to answer this question.",
                    "sources": []
                }

            return {
                "answer": answer,
                "sources": [{"text": selected_text[:200] + "..."}]  # Include truncated text as source
            }
        except Exception as e:
            logger.error(f"Error in selected text query: {e}")
            raise

    def _is_response_fallback(self, answer: str) -> bool:
        """
        Check if the response is a generic fallback that might indicate hallucination.
        This helps ensure constitutional compliance with grounded responses only.
        """
        fallback_indicators = [
            "sorry",
            "i don't know",
            "there is no information",
            "not mentioned in the text",
            "not specified in the context",
            "cannot determine",
            "no information provided",
            "not provided in the context"
        ]

        answer_lower = answer.lower()
        for indicator in fallback_indicators:
            if indicator in answer_lower:
                # Check if it's the exact failure message we want
                if "does not contain enough information" in answer_lower:
                    return False  # This is the acceptable failure response
                return True  # This is a different kind of fallback/hallucination

        return False

    async def close(self):
        """Cleanup resources"""
        await self.cohere_client.close()
        # Close Qdrant client connection pool
        if hasattr(self.qdrant_client, '_client') and hasattr(self.qdrant_client._client, 'close'):
            await self.qdrant_client._client.close()