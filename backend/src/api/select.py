from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from src.services.rag_service import RAGService
from src.database.database import get_rag_service

router = APIRouter()

class SelectRequest(BaseModel):
    question: str
    selected_text: str
    session_id: Optional[str] = None

class SourceReference(BaseModel):
    text: str

class SelectResponse(BaseModel):
    answer: str
    sources: List[SourceReference]

@router.post("/select", response_model=SelectResponse)
async def select_endpoint(
    request: SelectRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Handle a query using only the selected text as context.
    Global vector search is disabled; only uses provided selected text.
    """
    try:
        result = await rag_service.query_selected_text(
            question=request.question,
            selected_text=request.selected_text,
            session_id=request.session_id
        )
        return SelectResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))