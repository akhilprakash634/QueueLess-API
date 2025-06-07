from fastapi import APIRouter
from app.schemas.feedback import Feedback, FeedbackCreate
from app.db import db
from datetime import datetime
from typing import List

router = APIRouter(prefix="/locations", tags=["Feedback"])


@router.post("/{location_id}/feedback", response_model=Feedback)
def submit_feedback(location_id: str, feedback: FeedbackCreate):
    fb = {
        "location_id": location_id,
        "timestamp": datetime.utcnow(),
        **feedback.dict()
    }
    db.collection("feedback").add(fb)
    return Feedback(**fb)


@router.get("/{location_id}/feedback", response_model=List[Feedback])
def get_feedback(location_id: str):
    docs = db.collection("feedback").where("location_id", "==", location_id).stream()
    return [Feedback(**doc.to_dict()) for doc in docs]
