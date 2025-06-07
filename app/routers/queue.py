from fastapi import APIRouter
from app.schemas.queue import QueueUpdateCreate, QueueUpdate
from app.db import db
from datetime import datetime
from typing import List

router = APIRouter(prefix="/locations", tags=["Queue Updates"])


@router.post("/{location_id}/update", response_model=QueueUpdate)
def update_queue(location_id: str, data: QueueUpdateCreate):
    update = {
        "location_id": location_id,
        "timestamp": datetime.utcnow(),
        **data.dict()
    }
    ref = db.collection("queue_updates").document()
    ref.set(update)
    return QueueUpdate(**update)


@router.get("/{location_id}/queue-history", response_model=List[QueueUpdate])
def get_queue_history(location_id: str):
    docs = db.collection("queue_updates").where("location_id", "==", location_id).stream()
    return [QueueUpdate(**doc.to_dict()) for doc in docs]
