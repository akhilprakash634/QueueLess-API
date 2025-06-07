from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FeedbackCreate(BaseModel):
    user_id: str
    rating: int
    comment: Optional[str] = None


class Feedback(BaseModel):
    location_id: str
    user_id: str
    rating: int
    comment: Optional[str] = None
    timestamp: datetime
