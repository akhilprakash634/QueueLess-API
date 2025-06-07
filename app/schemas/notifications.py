from pydantic import BaseModel
from typing import List


class NotificationRegister(BaseModel):
    user_id: str
    device_token: str
    subscribed_to: List[str]


class Notification(BaseModel):
    user_id: str
    device_token: str
    subscribed_to: List[str]
