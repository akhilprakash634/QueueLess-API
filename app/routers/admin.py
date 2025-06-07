from fastapi import APIRouter, HTTPException
from app.db import db

router = APIRouter(prefix="/admin", tags=["Admin Tools"])

@router.get("/overview")
def get_admin_overview():
    return {
        "total_users": len(list(db.collection("users").stream())),
        "total_locations": len(list(db.collection("locations").stream())),
        "total_updates": len(list(db.collection("queue_updates").stream())),
        "total_feedback": len(list(db.collection("feedback").stream())),
    }

@router.get("/reports/download")
def download_reports():
    return {
        "message": "Mock report generated",
        "report": {
            "users": len(list(db.collection("users").stream())),
            "updates": len(list(db.collection("queue_updates").stream())),
            "feedback": len(list(db.collection("feedback").stream())),
        }
    }

@router.put("/users/{user_id}/role")
def update_user_role(user_id: str, role: str):
    ref = db.collection("users").document(user_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")
    ref.update({"role": role})
    return {"message": f"Role updated to {role}"}

@router.get("/contributions")
def get_contributions():
    updates = db.collection("queue_updates").stream()
    feedbacks = db.collection("feedback").stream()

    from collections import defaultdict
    user_updates = defaultdict(int)
    user_feedback = defaultdict(int)

    for u in updates:
        data = u.to_dict()
        user_updates[data.get("updated_by")] += 1

    for f in feedbacks:
        data = f.to_dict()
        user_feedback[data.get("user_id")] += 1

    return {
        "queue_updates": dict(user_updates),
        "feedback": dict(user_feedback),
    }
