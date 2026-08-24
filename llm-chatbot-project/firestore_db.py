"""
Simple helper functions to save and load chat history from Firestore.

If Firebase did not connect (db is None), save_message() does nothing and
get_conversation() returns an empty list. This means the chatbot keeps
working even without Firestore.

Firestore structure:

conversations/
    {session_id}/
        messages/
            {auto_id}/
                user_message
                bot_reply
                timestamp
"""

from datetime import datetime, timezone

import config
from firebase_config import db


def save_message(session_id, user_message, bot_reply):
    """Save one user/bot exchange to Firestore. Fails silently if Firebase is unavailable."""
    if db is None:
        return

    try:
        messages_ref = (
            db.collection(config.FIRESTORE_COLLECTION)
            .document(session_id)
            .collection("messages")
        )
        messages_ref.add({
            "user_message": user_message,
            "bot_reply": bot_reply,
            "timestamp": datetime.now(timezone.utc),
        })
    except Exception as e:
        print(f"[Firestore] Failed to save message: {e}")


def get_conversation(session_id, limit=None):
    """Return this session's message history as a list of dicts, oldest first."""
    if db is None:
        return []

    limit = limit or config.MAX_HISTORY_TURNS

    try:
        messages_ref = (
            db.collection(config.FIRESTORE_COLLECTION)
            .document(session_id)
            .collection("messages")
            .order_by("timestamp")
            .limit_to_last(limit)
        )
        docs = messages_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[Firestore] Failed to load conversation: {e}")
        return []
