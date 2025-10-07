from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    file_name: Optional[str]
    page_number: Optional[int]
    score: Optional[float]
    created_at: datetime

    model_config = {
        "from_attributes": True 
    }

class ChatSessionResponse(BaseModel):
    id: int
    session_name: Optional[str]
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    model_config = {
        "from_attributes": True
    }
