from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.locations import Location, LocationCreate, LocationUpdate
from app.db import db
from datetime import datetime

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/", response_model=List[Location])
def list_locations():
    docs = db.collection("locations").stream()
    return [Location(id=doc.id, **doc.to_dict()) for doc in docs]

@router.get("/{location_id}", response_model=Location)
def get_location(location_id: str):
    doc = db.collection("locations").document(location_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location(id=doc.id, **doc.to_dict())

@router.post("/", response_model=Location)
def create_location(location: LocationCreate):
    ref = db.collection("locations").document()
    data = location.dict()
    data["updated_at"] = datetime.utcnow().isoformat()
    ref.set(data)
    return Location(id=ref.id, **data)

@router.put("/{location_id}", response_model=Location)
def update_location(location_id: str, update: LocationUpdate):
    ref = db.collection("locations").document(location_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Location not found")
    current = doc.to_dict()
    current.update(update.dict(exclude_unset=True))
    current["updated_at"] = datetime.utcnow().isoformat()
    ref.set(current)
    return Location(id=location_id, **current)

@router.delete("/{location_id}")
def delete_location(location_id: str):
    ref = db.collection("locations").document(location_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Location not found")
    ref.delete()
    return {"message": "Location deleted"}
