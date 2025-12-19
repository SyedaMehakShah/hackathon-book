import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import AsyncOpenAI
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Initialize Qdrant client - try local first, then in-memory if that fails
        try:
            # Connect to Qdrant instance (this could be local or cloud)
            self.qdrant_client = QdrantClient(
                url=os.getenv("QDRANT_HOST", "http://localhost:6333"),
                api_key=os.getenv("QDRANT_API_KEY")
            )
            logger.info("Connected to Qdrant instance")
        except Exception as e:
            # If connection fails, use in-memory client
            logger.warning(f"Could not connect to Qdrant host: {e}. Using in-memory storage.")
            self.qdrant_client = QdrantClient(":memory:")
            logger.info("Initialized in-memory Qdrant client")

        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Collection name
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

        # Initialize the collection if it doesn't exist
        try:
            # Try to get the collection, ignore errors during the check
            try:
                self.qdrant_client.get_collection(self.collection_name)
                logger.info(f"Collection '{self.collection_name}' already exists")
            except Exception:
                # Create collection if it doesn't exist
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.warning(f"Could not create or access collection '{self.collection_name}': {e}")
            # Try to create collection with a simpler vector config
            try:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
                )
                logger.info(f"Created collection with fallback method: {self.collection_name}")
            except Exception as fallback_e:
                logger.error(f"Fallback collection creation also failed: {fallback_e}")
                raise

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for the given text using OpenAI
        """
        try:
            response = await self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def store_document(self, content: str, content_id: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store a document in the vector database
        """
        try:
            # Generate embedding
            embedding = await self.embed_text(content)
            
            # Prepare the point
            point = models.PointStruct(
                id=content_id,
                vector=embedding,
                payload={
                    "content": content,
                    "content_id": content_id,
                    **(metadata or {})
                }
            )
            
            # Store in Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Stored document {content_id} in vector database")
            return True
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return False

    async def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents relevant to the query
        """
        try:
            # Generate embedding for the query
            query_embedding = await self.embed_text(query)
            
            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )
            
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "relevance_score": result.score,
                    "metadata": {k: v for k, v in result.payload.items() if k not in ["content", "content_id"]}
                })
            
            logger.info(f"Found {len(results)} results for query")
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    async def answer_question(self, question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Answer a question using the RAG system
        """
        try:
            # Search for relevant documents
            search_results = await self.search_documents(question)
            
            if not search_results:
                return {
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Prepare context from search results
            contexts = [result["content"] for result in search_results]
            combined_context = "\n\n".join(contexts)
            
            # Optionally include additional context passed by the user
            if context:
                combined_context = f"{context}\n\n{combined_context}"
            
            # Prepare the prompt for OpenAI
            prompt = f"""
            You are an assistant for the Physical AI & Humanoid Robotics textbook. 
            Use the following context to answer the question. 
            If the context doesn't contain the answer, say so.
            
            Context: {combined_context}
            
            Question: {question}
            
            Answer:
            """
            
            # Get answer from OpenAI
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant for the Physical AI & Humanoid Robotics textbook. Provide helpful and accurate answers based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Extract sources
            sources = [result["id"] for result in search_results]
            
            # For confidence, we'll use the highest relevance score
            max_score = max([result["relevance_score"] for result in search_results])
            confidence = min(max_score, 1.0)  # Normalize to 0-1 range
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "answer": "An error occurred while processing your question. Please try again.",
                "sources": [],
                "confidence": 0.0
            }

    async def answer_from_highlighted_text(self, highlighted_text: str, question: str) -> Dict[str, Any]:
        """
        Answer a question based on highlighted text
        """
        try:
            # Use the highlighted text as the primary context
            prompt = f"""
            You are an assistant for the Physical AI & Humanoid Robotics textbook.
            Answer the question based on the following highlighted text:

            Highlighted text: {highlighted_text}

            Question: {question}

            Answer:
            """

            # Get answer from OpenAI
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant for the Physical AI & Humanoid Robotics textbook. Provide helpful and accurate answers based on the provided highlighted text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )

            answer = response.choices[0].message.content.strip()

            return {
                "answer": answer,
                "explanation": f"The answer is based on the highlighted text: {highlighted_text[:100]}..."
            }
        except Exception as e:
            logger.error(f"Error answering from highlighted text: {e}")
            return {
                "answer": "An error occurred while processing your question. Please try again.",
                "explanation": "An error occurred"
            }

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of available tools for the RAG system
        """
        return [
            {
                "name": "search_textbook",
                "description": "Search the textbook content for information related to the query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results to return (default 5)"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

    async def call_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        """
        Execute a specific tool with the provided arguments
        """
        if tool_name == "search_textbook":
            query = tool_args.get("query", "")
            top_k = tool_args.get("top_k", 5)
            return await self.search_documents(query, top_k)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def close(self):
        """
        Close the RAG service and clean up resources
        """
        try:
            # Close the Qdrant client if it has a close method
            if hasattr(self.qdrant_client, 'close'):
                self.qdrant_client.close()
            logger.info("RAG service closed successfully")
        except Exception as e:
            logger.error(f"Error closing RAG service: {e}")
            raise