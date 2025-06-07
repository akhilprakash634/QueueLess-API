from pydantic import BaseModel
from typing import Optional


class Geo(BaseModel):
    lat: float
    lng: float


class LocationBase(BaseModel):
    name: str
    type: str
    location: str
    geo: Geo


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    geo: Optional[Geo] = None


class Location(LocationBase):
    id: str
    active_token: Optional[int] = None
    updated_by: Optional[str] = None
    updated_at: Optional[str] = None
