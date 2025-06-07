from fastapi import APIRouter, HTTPException
from app.schemas.users import User, UserHistory
from app.db import db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=User)
def get_current_user():
    user = next(db.collection("users").limit(1).stream(), None)
    if not user:
        raise HTTPException(status_code=404, detail="No users")
    return User(id=user.id, **user.to_dict())

@router.get("/{user_id}/history", response_model=UserHistory)
def get_user_history(user_id: str):
    updates = db.collection("queue_updates").where("updated_by", "==", user_id).stream()
    feedbacks = db.collection("feedback").where("user_id", "==", user_id).stream()
    return {
        "updates": [u.to_dict() for u in updates],
        "feedback": [f.to_dict() for f in feedbacks]
    }
