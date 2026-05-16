import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from backend.confidence.confidence_engine import get_confidence_level
from backend.database.chat_db import save_chat
from backend.database.failure_db import save_failure
from backend.database.init_db import initialize_database
from backend.database.user_db import create_user, verify_user
from backend.failure.failure_detector import detect_failure
from backend.ml.emotion_engine import detect_emotion
from backend.ml.intent_engine import predict_intent
from backend.response.response_generator import generate_response

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
serializer = URLSafeTimedSerializer(app.secret_key)
CORS(app, supports_credentials=True)

initialize_database()


@app.get("/")
def serve_home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/<page>.html")
def serve_page(page: str):
    allowed = {"login", "signup", "chat"}
    if page not in allowed:
        return send_from_directory(FRONTEND_DIR, "index.html")
    return send_from_directory(FRONTEND_DIR, f"{page}.html")


def _token_for(username: str) -> str:
    return serializer.dumps({"username": username})


def _username_from_token(token: str) -> str | None:
    try:
        data = serializer.loads(token, max_age=60 * 60 * 24 * 7)
        return data.get("username")
    except (BadSignature, SignatureExpired):
        return None


def _auth_username() -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return _username_from_token(auth[7:].strip())
    return None


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/auth/signup")
def signup():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    ok, message = create_user(username, password)
    if not ok:
        return jsonify({"error": message}), 400

    username = username.lower()
    return jsonify(
        {
            "message": message,
            "token": _token_for(username),
            "username": username,
        }
    )


@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    ok, result = verify_user(username, password)
    if not ok:
        return jsonify({"error": result}), 401

    return jsonify(
        {
            "message": "Logged in successfully.",
            "token": _token_for(result),
            "username": result,
        }
    )


@app.get("/api/auth/me")
def me():
    username = _auth_username()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"username": username})


@app.post("/api/chat")
def chat():
    username = _auth_username()
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    intent, probability = predict_intent(user_message)
    emotion = detect_emotion(user_message)
    confidence = get_confidence_level(probability)
    bot_response = generate_response(
        user_message, intent, confidence, emotion
    )
    failed = detect_failure(confidence, emotion)

    save_chat(
        username=username,
        user_message=user_message,
        bot_response=bot_response,
        intent=intent,
        emotion=emotion,
        confidence=confidence,
    )

    if failed:
        save_failure(
            username=username,
            user_message=user_message,
            bot_response=bot_response,
            reason="Low confidence or negative emotion",
        )

    return jsonify(
        {
            "response": bot_response,
            "intent": intent,
            "emotion": emotion,
            "confidence": confidence,
            "failed": failed,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
