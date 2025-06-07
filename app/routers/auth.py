from fastapi import APIRouter, HTTPException
from app.schemas.users import UserCreate, User
from app.db import db
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=User)
def signup(user: UserCreate):
    existing = list(db.collection("users").where("email", "==", user.email).stream())
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "email": user.email,
        "role": "User",
        "points": 0,
        "registered_at": datetime.utcnow()
    }
    ref = db.collection("users").document()
    ref.set(user_data)
    return User(id=ref.id, **user_data)


@router.post("/login", response_model=User)
def login(user: UserCreate):
    docs = db.collection("users").where("email", "==", user.email).stream()
    for doc in docs:
        return User(id=doc.id, **doc.to_dict())
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/google", response_model=User)
def google_login():
    return {"message": "Google login not implemented in mock version"}
