from fastapi import APIRouter, HTTPException
from app.schemas.rewards import Rewards, RedemptionItem
from app.db import db
from datetime import date
from typing import List

router = APIRouter(prefix="/rewards", tags=["Rewards"])

@router.get("/me", response_model=Rewards)
def get_my_rewards():
    user_doc = next(db.collection("users").limit(1).stream(), None)
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    uid = user_doc.id
    reward_doc = db.collection("rewards").document(uid).get()

    if reward_doc.exists:
        return Rewards(**reward_doc.to_dict())

    default = {
        "user_id": uid,
        "points_earned": 0,
        "redeemed_items": []
    }
    db.collection("rewards").document(uid).set(default)
    return Rewards(**default)

@router.post("/redeem", response_model=Rewards)
def redeem_item(item: str, points: int):
    user_doc = next(db.collection("users").limit(1).stream(), None)
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    uid = user_doc.id
    ref = db.collection("rewards").document(uid)
    reward_doc = ref.get()

    if not reward_doc.exists:
        raise HTTPException(status_code=404, detail="Rewards not found")

    data = reward_doc.to_dict()

    if data["points_earned"] < points:
        raise HTTPException(status_code=400, detail="Not enough points")

    data["points_earned"] -= points
    data["redeemed_items"].append({
        "item": item,
        "points": points,
        "date": date.today().isoformat()
    })
    ref.set(data)
    return Rewards(**data)

@router.get("/leaderboard", response_model=List[Rewards])
def get_leaderboard():
    docs = db.collection("rewards").stream()
    rewards_list = [Rewards(**doc.to_dict()) for doc in docs]
    return sorted(rewards_list, key=lambda r: r.points_earned, reverse=True)
