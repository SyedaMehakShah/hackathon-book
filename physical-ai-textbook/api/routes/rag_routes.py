from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from uuid import UUID

from models.base import ChatSession, ChatSessionCreate, VectorDocument
from services.rag_service import RAGService
from services.vector_db_service import VectorDBService
from services.document_ingestion_service import DocumentIngestionService

# Create router
router = APIRouter()

# Initialize services
# Using a lazy initialization approach to handle Qdrant connection issues
rag_service = None
vector_db_service = VectorDBService()
ingestion_service = None

# In-memory storage for demo purposes (will be replaced with database)
chat_sessions_db = {}

class EmbedRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class EmbedResponse(BaseModel):
    document_id: str
    success: bool

class StoreRequest(BaseModel):
    content: str
    content_id: str
    metadata: Optional[Dict[str, Any]] = None

class StoreResponse(BaseModel):
    document_id: str
    success: bool

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

class AskRequest(BaseModel):
    question: str
    context: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class AnswerHighlightedRequest(BaseModel):
    highlighted_text: str
    question: str

class AnswerHighlightedResponse(BaseModel):
    answer: str
    explanation: str

@router.post("/embed", response_model=EmbedResponse)
async def embed_content(request: EmbedRequest):
    """
    Embed content for storage in vector database
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        # Generate embedding using the RAG service
        embedding = await rag_service.embed_text(request.content)

        # Store in vector database
        doc_id = request.metadata.get("id", str(uuid.uuid4())) if request.metadata else str(uuid.uuid4())
        success = await rag_service.store_document(
            content=request.content,
            content_id=doc_id,
            metadata=request.metadata
        )

        return EmbedResponse(
            document_id=doc_id,
            success=success
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding content: {str(e)}")

@router.post("/store", response_model=StoreResponse)
async def store_content(request: StoreRequest):
    """
    Store content in the vector database
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        success = await rag_service.store_document(
            content=request.content,
            content_id=request.content_id,
            metadata=request.metadata
        )

        return StoreResponse(
            document_id=request.content_id,
            success=success
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing content: {str(e)}")

@router.get("/search", response_model=SearchResponse)
async def search_content(query: str, top_k: int = 5):
    """
    Search textbook content
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        results = await rag_service.search_documents(query, top_k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching content: {str(e)}")

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Ask a question to the RAG chatbot
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        result = await rag_service.answer_question(request.question, request.context)
        return AskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@router.post("/answer-highlighted", response_model=AnswerHighlightedResponse)
async def answer_from_highlighted_text(request: AnswerHighlightedRequest):
    """
    Answer a question based on selected/highlighted text
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        result = await rag_service.answer_from_highlighted_text(
            request.highlighted_text,
            request.question
        )
        return AnswerHighlightedResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering from highlighted text: {str(e)}")

@router.post("/chat", response_model=ChatSession)
async def create_chat_session(chat_data: ChatSessionCreate = None):
    """
    Create a new chat session with the RAG chatbot
    """
    session_id = str(uuid.uuid4())

    # Create a new session
    session = {
        "id": session_id,
        "userId": chat_data.userId if chat_data else None,
        "startedAt": datetime.now().isoformat(),
        "lastMessageAt": datetime.now().isoformat(),
        "messages": [],
        "context": None
    }

    chat_sessions_db[session_id] = session

    return ChatSession(
        id=UUID(session_id),
        userId=chat_data.userId if chat_data else None,
        startedAt=datetime.fromisoformat(session["startedAt"]),
        lastMessageAt=datetime.fromisoformat(session["lastMessageAt"]),
        messages=session["messages"],
        context=session["context"]
    )

@router.get("/chat/history")
async def get_chat_history(session_id: str):
    """
    Retrieve chat history for a session
    """
    if session_id not in chat_sessions_db:
        raise HTTPException(status_code=404, detail="Chat session not found")

    return chat_sessions_db[session_id]["messages"]

@router.post("/ingest-book")
async def ingest_entire_book():
    """
    Ingest the entire textbook into the vector database
    """
    global rag_service, ingestion_service
    try:
        # Initialize services if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        success = await ingestion_service.process_and_ingest_book()
        if success:
            return {"message": "Successfully ingested the entire textbook", "success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest the textbook")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting textbook: {str(e)}")

@router.post("/index-textbook-content")
async def index_textbook_content():
    """
    Index all textbook content in the vector database with chunking and metadata
    """
    global rag_service, ingestion_service
    try:
        # Initialize services if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        # Get all markdown files from the docs directory
        import os
        from pathlib import Path

        docs_path = Path("C:/Users/Admin/hackathon/physical-ai-textbook/docs")
        if not docs_path.exists():
            raise HTTPException(status_code=404, detail="Docs directory not found")

        # Process each markdown file
        processed_count = 0
        for md_file in docs_path.rglob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Create chunks for long documents
            chunks = await ingestion_service.chunk_text(
                content,
                chunk_size=1000,
                overlap=100
            )

            # Add metadata about the source
            source_metadata = {
                "source_file": str(md_file.relative_to(docs_path)),
                "file_path": str(md_file),
                "type": "textbook_content"
            }

            # Process each chunk
            for chunk in chunks:
                chunk_metadata = {**chunk.get("metadata", {}), **source_metadata}

                success = await rag_service.store_document(
                    content=chunk["text"],
                    content_id=chunk["id"],
                    metadata=chunk_metadata
                )

                if success:
                    processed_count += 1

        return {
            "message": f"Successfully indexed textbook content",
            "documents_processed": processed_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing textbook content: {str(e)}")

class QueryGlobalRequest(BaseModel):
    question: str
    book_id: str
    session_id: Optional[str] = None

class QueryGlobalResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []
    confidence: Optional[float] = 0.0

@router.post("/rag/query-global", response_model=QueryGlobalResponse)
async def query_global(request: QueryGlobalRequest):
    """
    Global query endpoint designed to work with textbook content
    """
    global rag_service, ingestion_service
    try:
        # Initialize rag_service if not already done
        if rag_service is None:
            rag_service = RAGService()
            ingestion_service = DocumentIngestionService(rag_service, vector_db_service)

        # For now, we'll use the regular answer_question method
        # In a full implementation, we might want to add book_id-specific filtering
        result = await rag_service.answer_question(request.question)

        return QueryGlobalResponse(
            answer=result.get('answer', ''),
            sources=result.get('sources', []),
            confidence=result.get('confidence', 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing global query: {str(e)}")

# Legacy endpoint for compatibility with frontend implementation
@router.post("/v1/rag/query-global", response_model=QueryGlobalResponse)
async def query_global_legacy(request: QueryGlobalRequest):
    """
    Legacy global query endpoint with version prefix
    """
    return await query_global(request)