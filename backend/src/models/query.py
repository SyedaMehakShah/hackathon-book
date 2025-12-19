from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .chunk import Chunk

class Query(BaseModel):
    query_id: str
    session_id: str
    question: str
    response: str
    chunks_used: List[Chunk]
    timestamp: datetime
    mode: str  # "global" or "selected_text"
    metadata: Optional[dict] = None