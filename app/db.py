import os
from google.cloud import firestore

firebase_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not firebase_path:
    raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS env variable")

db = firestore.Client.from_service_account_json(firebase_path)
