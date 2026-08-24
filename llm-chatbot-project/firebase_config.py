"""
Sets up the connection to Firebase Firestore.

If the credentials file is missing or invalid, `db` stays None and the
rest of the app keeps working WITHOUT chat history persistence. Nothing
here should ever crash the chatbot.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

import config

db = None

try:
    if os.path.exists(config.FIREBASE_CREDENTIALS_PATH):
        cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("[Firestore] Connected - chat history will be persisted.")
    else:
        print("[Firestore] Not initialized, persistence disabled.")
        print(f"  (No credentials file found at '{config.FIREBASE_CREDENTIALS_PATH}')")
except Exception as e:
    print("[Firestore] Not initialized, persistence disabled.")
    print(f"  (Error: {e})")
    db = None
