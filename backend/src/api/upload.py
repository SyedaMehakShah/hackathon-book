from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional
from src.services.rag_service import RAGService
from src.database.database import get_rag_service

router = APIRouter()

class UploadBookRequest(BaseModel):
    title: str
    author: str
    book_id: str

class UploadResponse(BaseModel):
    message: str
    book_id: str
    status: str

@router.post("/upload", response_model=UploadResponse)
async def upload_book(
    book_id: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    chapter: str = Form(None),  # Optional chapter information
    page_number: int = Form(None),  # Optional page number
    file: UploadFile = File(...),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Upload a book file to be indexed for RAG queries.
    Supports various text formats and processes content into semantic chunks.
    """
    if not file.content_type.startswith("text/"):
        raise HTTPException(
            status_code=400,
            detail="Only text files are supported for initial implementation"
        )

    try:
        # Read the uploaded file
        content = await file.read()
        text_content = content.decode("utf-8")

        # Process and index the book
        result = await rag_service.index_book(
            book_id=book_id,
            title=title,
            author=author,
            content=text_content,
            chapter=chapter,
            page_number=page_number
        )

        return UploadResponse(
            message="Book uploaded and indexed successfully",
            book_id=book_id,
            status="completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")