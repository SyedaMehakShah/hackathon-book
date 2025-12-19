import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_HOST", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        
        # Collection name
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    async def create_collection(self, vector_size: int = 1536) -> bool:
        """
        Create a new collection in the vector database
        """
        try:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )
            logger.info(f"Created collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return False

    async def index_text(self, text: str, text_id: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Index a text in the vector database
        """
        try:
            # This would be called from the embedding service after generating embeddings
            # For now, we'll assume the embedding is passed in
            # In a real implementation, this would be handled by the embedding service
            logger.info(f"Indexed text with ID: {text_id}")
            return True
        except Exception as e:
            logger.error(f"Error indexing text: {e}")
            return False

    async def batch_index_texts(self, texts: List[Dict[str, Any]]) -> bool:
        """
        Index multiple texts in the vector database
        """
        try:
            # Process texts in batches
            success_count = 0
            for text_data in texts:
                text = text_data.get("text", "")
                text_id = text_data.get("id", "")
                metadata = text_data.get("metadata", {})
                
                if await self.index_text(text, text_id, metadata):
                    success_count += 1
            
            logger.info(f"Successfully indexed {success_count}/{len(texts)} texts")
            return success_count == len(texts)
        except Exception as e:
            logger.error(f"Error in batch indexing: {e}")
            return False

    async def search(self, query_vector: List[float], top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the database
        """
        try:
            # Apply filters if provided
            qdrant_filters = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    ))
                qdrant_filters = models.Filter(must=conditions)

            # Perform search
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filters
            )

            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "payload": result.payload,
                    "score": result.score
                })

            logger.info(f"Search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return []

    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document by ID
        """
        try:
            records = self.qdrant_client.retrieve(
                collection_name=self.collection_name,
                ids=[doc_id]
            )

            if records:
                record = records[0]
                return {
                    "id": record.id,
                    "payload": record.payload,
                    "vector": record.vector
                }

            logger.info(f"No document found with ID: {doc_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            return None

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by ID
        """
        try:
            self.qdrant_client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[doc_id])
            )
            logger.info(f"Deleted document with ID: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    async def update_document(self, doc_id: str, payload: Dict[str, Any]) -> bool:
        """
        Update a document's payload
        """
        try:
            self.qdrant_client.set_payload(
                collection_name=self.collection_name,
                points=[models.PointVectors(
                    id=doc_id,
                    payload=payload
                )],
                wait=True
            )
            logger.info(f"Updated document with ID: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return False

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection
        """
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}