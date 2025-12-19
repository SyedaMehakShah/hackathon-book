import os
import json
import logging
import asyncio
from typing import List, Dict, Any
from pathlib import Path
import re
import uuid

import cohere
from qdrant_client import AsyncQdrantClient, models
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookChatbot:
    def __init__(self):
        # Initialize API clients
        self.cohere_client = cohere.AsyncClient(os.getenv("COHERE_API_KEY"))
        
        # Initialize Qdrant client
        self.qdrant_client = AsyncQdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            timeout=10
        )
        
        # Collection name
        self.collection_name = "book_chunks"
        
        # Track document IDs to ensure uniqueness
        self.doc_id_counter = 0
        
    async def close_connections(self):
        """Close connections to API clients"""
        logger.info("Closing connections...")
        await self.qdrant_client.close()
        await self.cohere_client.close()

    async def initialize_collection(self):
        """Create the Qdrant collection if it doesn't exist"""
        try:
            collections = await self.qdrant_client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            
            if not collection_exists:
                logger.info(f"Creating collection '{self.collection_name}'")
                
                # Get embedding dimension from Cohere (for English-3-multilingual, it's 1024)
                sample_embedding = await self.cohere_client.embed(
                    texts=["sample text"],
                    model="embed-english-v3.0",
                    input_type="search_document"
                )
                embedding_size = len(sample_embedding.embeddings[0])
                
                await self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=embedding_size,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Collection '{self.collection_name}' created successfully")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    async def chunk_markdown_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split markdown content into chunks of appropriate size
        """
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed the max size
            if len(current_chunk) + len(paragraph) > max_chunk_size:
                if current_chunk:  # If we have accumulated text, save it as a chunk
                    chunks.append(current_chunk.strip())
                # Start new chunk with the current paragraph
                current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the final remaining chunk if there's any content left
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If any individual chunk is still too large, split it by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_chunk_size:
                # Split large chunk by sentences
                sentences = re.split(r'[.!?]+', chunk)
                temp_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(temp_chunk) + len(sentence) > max_chunk_size:
                        if temp_chunk:
                            final_chunks.append(temp_chunk.strip())
                        temp_chunk = sentence
                    else:
                        if temp_chunk:
                            temp_chunk += " " + sentence
                        else:
                            temp_chunk = sentence
                
                if temp_chunk:
                    final_chunks.append(temp_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        # Filter out empty chunks
        final_chunks = [chunk for chunk in final_chunks if chunk.strip()]
        
        return final_chunks

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text with retry logic"""
        try:
            response = await self.cohere_client.embed(
                texts=[text],
                model="embed-english-v3.0",
                input_type="search_query"  # Using search_query for user queries
            )
            return response.embeddings[0]
        except Exception as e:
            logger.warning(f"Embedding failed, retrying: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents with retry logic"""
        try:
            response = await self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            logger.warning(f"Batch embedding failed, retrying: {e}")
            raise

    async def index_documents_from_json(self, json_path: str):
        """Index all documents from a JSON file containing extracted docs"""
        logger.info(f"Indexing documents from {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        # Prepare points for batch insertion
        points = []
        doc_count = 0
        
        for doc in documents:
            content = doc.get('cleaned_content', doc.get('content', ''))
            file_path = doc.get('file_path', 'unknown')
            chapter = doc.get('chapter', 'unknown')
            
            # Chunk the document content
            chunks = await self.chunk_markdown_content(content)
            
            logger.info(f"Chunking document {file_path}: {len(chunks)} chunks created")
            
            # Embed all chunks in batches
            batch_size = 10  # Cohere free tier limits
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                
                try:
                    embeddings = await self.embed_documents(batch_chunks)
                    
                    # Create points for Qdrant
                    for j, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
                        point_id = self.doc_id_counter
                        
                        payload = {
                            "content": chunk,
                            "file_path": file_path,
                            "chapter": chapter,
                            "chunk_index": j
                        }
                        
                        points.append(
                            models.PointStruct(
                                id=point_id,
                                vector=embedding,
                                payload=payload
                            )
                        )
                        
                        self.doc_id_counter += 1
                        
                        # Log progress every 100 points added
                        if len(points) % 100 == 0:
                            logger.info(f"Processed {len(points)} document chunks...")
                
                except Exception as e:
                    logger.error(f"Failed to embed batch: {e}")
                    continue
        
        # Batch upload to Qdrant
        if points:
            logger.info(f"Uploading {len(points)} points to Qdrant...")
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Successfully indexed {len(points)} document chunks")
        
        logger.info(f"Total documents processed: {doc_count}")

    async def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant chunks from Qdrant"""
        try:
            query_embedding = await self.embed_text(query)
            
            search_results = await self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )
            
            results = []
            for hit in search_results:
                result = {
                    'id': hit.id,
                    'score': hit.score,
                    'content': hit.payload.get('content', ''),
                    'file_path': hit.payload.get('file_path', ''),
                    'chapter': hit.payload.get('chapter', ''),
                    'chunk_index': hit.payload.get('chunk_index', 0)
                }
                results.append(result)
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    def display_context(self, results: List[Dict[str, Any]]):
        """Display the retrieved context chunks"""
        print("\n" + "="*60)
        print("RETRIEVED CONTEXT CHUNKS:")
        print("="*60)

        for i, result in enumerate(results, 1):
            print(f"\nChunk {i} (Score: {result['score']:.4f})")
            print(f"Chapter: {result['chapter']}")
            print(f"File: {result['file_path']}")
            print(f"Content Preview: {result['content'][:500]}...")
            if len(result['content']) > 500:
                print("...")

        print("="*60)

    async def generate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Placeholder function for LLM-based response generation using retrieved context.
        This function could call an LLM service with the context and query to generate a response.
        """
        # For now, return a placeholder response
        return "This is a placeholder for the LLM-generated response. In a full implementation, an LLM would process the query along with the retrieved context chunks to generate a comprehensive answer."

    async def start_chat(self):
        """Start the chatbot loop"""
        print("Book Content Chatbot Initialized!")
        print("Enter your questions about the book content, or type 'quit' to exit.")
        print("Type 'rebuild-index' to reindex the documents (this will take a moment).")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\nYour question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Thank you for using the Book Content Chatbot. Goodbye!")
                    break
                elif user_input.lower() == 'rebuild-index':
                    print("Rebuilding index...")
                    await self.initialize_collection()
                    await self.index_documents_from_json('extracted_docs_content.json')
                    print("Index rebuilt successfully!")
                    continue
                
                if not user_input:
                    continue

                # Retrieve relevant context from Qdrant
                print("Retrieving relevant information...")
                context_results = await self.retrieve_context(user_input)

                if not context_results:
                    print("No relevant context found for your query.")
                    continue

                # Display the retrieved context
                self.display_context(context_results)

                # Generate response using the context
                # (Currently just a placeholder - can be enhanced with LLM call)
                response = await self.generate_response(user_input, context_results)

                print(f"\nChatbot Response: {response}")

            except KeyboardInterrupt:
                print("\n\nChatbot interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error during chat: {e}")
                print(f"An error occurred: {e}")


async def main():
    """Main function to run the chatbot"""
    # Initialize chatbot
    chatbot = BookChatbot()
    
    try:
        # Initialize the Qdrant collection
        await chatbot.initialize_collection()
        
        # Index the documents if not already done (or if needed)
        json_path = 'extracted_docs_content.json'  # This file exists in the current directory

        if os.path.exists(json_path):
            print("Indexing documents from JSON...")
            await chatbot.index_documents_from_json(json_path)
        else:
            logger.warning(f"Document file {json_path} not found. Proceeding without indexing.")
        
        # Start the chat loop
        await chatbot.start_chat()
    
    finally:
        # Always close connections when done
        await chatbot.close_connections()


if __name__ == "__main__":
    asyncio.run(main())