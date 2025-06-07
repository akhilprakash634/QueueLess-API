from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class QueueUpdateBase(BaseModel):
    token: int
    updated_by: str
    notes: Optional[str] = None


class QueueUpdateCreate(QueueUpdateBase):
    pass


class QueueUpdate(QueueUpdateBase):
    location_id: str
    timestamp: datetime
