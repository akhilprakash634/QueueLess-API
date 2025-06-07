from fastapi import APIRouter, HTTPException
from app.schemas.notifications import NotificationRegister, Notification
from app.db import db
from typing import List

router = APIRouter(tags=["Notifications"])

@router.post("/notifications/register", response_model=Notification)
def register_device(data: NotificationRegister):
    ref = db.collection("notifications").document(data.user_id)
    ref.set(data.dict())
    return data

@router.get("/notifications/me", response_model=List[Notification])
def get_my_notifications():
    user = next(db.collection("users").limit(1).stream(), None)
    if not user:
        raise HTTPException(status_code=404, detail="No users")
    uid = user.id
    docs = db.collection("notifications").where("user_id", "==", uid).stream()
    return [Notification(**doc.to_dict()) for doc in docs]

@router.post("/admin/notifications/send")
def send_push_to_users(message: str):
    count = len(list(db.collection("notifications").stream()))
    return {
        "message": f"Push sent to {count} devices.",
        "content": message
    }