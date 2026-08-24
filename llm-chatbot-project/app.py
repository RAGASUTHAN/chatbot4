"""
Flask backend for the chatbot website.

Routes:
  GET  /      -> serves the chat webpage (templates/index.html)
  POST /chat  -> receives {"message": "..."}, gets a reply from Gemini,
                 saves the exchange to Firestore, and returns
                 {"response": "..."}

Flow:
  Browser -> Flask -> Chatbot (chatbot.py) -> Gemini -> Flask -> Browser
  Flask also writes to Firestore (firestore_db.py) after each reply.
"""

import uuid

from flask import Flask, request, jsonify, render_template, session

import config
from chatbot import Chatbot
import firestore_db

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

bot = Chatbot()


@app.route("/")
def home():
    # Give every browser visitor a session id so their history stays separate.
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Request body must be JSON with a 'message' field."}), 400

    user_message = str(data["message"]).strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Use the browser's session id if there is one (website use).
    # Postman doesn't send cookies by default, so fall back to a fixed
    # id - this still lets you test /chat on its own.
    session_id = session.get("session_id", "postman-test-session")

    history = firestore_db.get_conversation(session_id)

    try:
        bot_reply = bot.get_response(user_message, history)
    except Exception:
        return jsonify({"error": "The chatbot failed to respond. Please try again."}), 500

    # Firebase is additive: if this fails, it's already handled inside
    # firestore_db.py and won't affect the response below.
    firestore_db.save_message(session_id, user_message, bot_reply)

    return jsonify({"response": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
