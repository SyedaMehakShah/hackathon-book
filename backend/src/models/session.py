from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

class Session(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    messages: List[Message]
    metadata: Optional[dict] = None