from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    role: str
    points: int
    registered_at: datetime


class UserHistory(BaseModel):
    updates: List[dict]
    feedback: List[dict]
