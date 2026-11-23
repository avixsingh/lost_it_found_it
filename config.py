"""Application configuration. Sensitive values come from environment variables (.env)."""
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    # If SECRET_KEY is missing a random one is used (sessions reset on restart).
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///lost_it_found_it.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Secure session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # set True when served over HTTPS
    REMEMBER_COOKIE_HTTPONLY = True

    # AI matching (similarity scores are indicative, NOT probabilities)
    AI_MODEL_NAME = "all-MiniLM-L6-v2"
    AI_ENABLED = os.environ.get("AI_ENABLED", "1") == "1"
    MATCH_THRESHOLD = float(os.environ.get("MATCH_THRESHOLD", "0.35"))
    MAX_MATCHES = int(os.environ.get("MAX_MATCHES", "5"))

    ITEMS_PER_PAGE = 9


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    AI_ENABLED = False  # tests use the keyword fallback unless they enable AI
    UPLOAD_FOLDER = str(BASE_DIR / "uploads" / "test")
