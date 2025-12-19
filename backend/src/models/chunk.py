from pydantic import BaseModel
from typing import Optional

class Chunk(BaseModel):
    chunk_id: str
    book_id: str
    content: str
    chapter: Optional[str] = None
    page_number: Optional[int] = None
    position: int  # Position in the book for ordering
    embedding: Optional[list] = None  # Will be stored in vector DB, not here
    metadata: Optional[dict] = None