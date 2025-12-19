from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from src.services.rag_service import RAGService
from src.database.database import get_rag_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    book_id: str
    session_id: Optional[str] = None

class SourceReference(BaseModel):
    chunk_id: str
    chapter: Optional[str] = None
    page_number: Optional[int] = None
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceReference]

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Handle a query against the book content using global RAG mode.
    Returns an answer grounded in the book content with source references.
    """
    try:
        result = await rag_service.query_global(
            question=request.question,
            book_id=request.book_id,
            session_id=request.session_id
        )
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))