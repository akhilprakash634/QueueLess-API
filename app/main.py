from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.db import db
from app.routers import locations, queue, feedback, auth, users, rewards, notifications, admin

app = FastAPI(title="QueueLess API", version="1.0")

# Include routers
app.include_router(locations.router)
app.include_router(queue.router)
app.include_router(feedback.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rewards.router)
app.include_router(notifications.router)
app.include_router(admin.router)

@app.get("/test-firestore")
def test_firestore():
    test_ref = db.collection("test_collection").document("test_doc")
    test_ref.set({"message": "hello from fastapi"})
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to QueueLess API"}
