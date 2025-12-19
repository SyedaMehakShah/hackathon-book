from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    upload_date: Optional[datetime] = None
    indexing_status: str = "pending"  # pending, processing, completed, failed
    total_chunks: Optional[int] = None
    metadata: Optional[dict] = None