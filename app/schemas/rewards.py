from pydantic import BaseModel
from typing import List
from datetime import date


class RedemptionItem(BaseModel):
    item: str
    points: int
    date: date


class Rewards(BaseModel):
    user_id: str
    points_earned: int
    redeemed_items: List[RedemptionItem]
