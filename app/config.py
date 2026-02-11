import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from peewee import MySQLDatabase
from app.db import database

load_dotenv()

def env(key: str, default: str = None) -> str:
    return os.getenv(key, default)

# 🗄️ Database
def env_db_uri() -> str:
    db_uri = env("DB_URI")
    if db_uri:
        return db_uri

    host = env("DB_HOST", "127.0.0.1")
    port = env("DB_PORT", "3306")
    name = env("DB_NAME", "lms")
    user = env("DB_USER", "root")
    password = env("DB_PASSWORD", "")
    return f"mysql://{user}:{password}@{host}:{port}/{name}"

def init_database_from_env() -> None:
    parsed = urlparse(env_db_uri())
    if parsed.scheme != "mysql":
        return
    name = (parsed.path or "/").lstrip("/") or None
    if not name:
        return
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 3306
    user = parsed.username or "root"
    password = parsed.password or ""
    database.initialize(MySQLDatabase(
        name,
        user=user,
        password=password,
        host=host,
        port=port,
        charset="utf8mb4",
    ))

SECRET_KEY = env("SECRET_KEY", "changeme")

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")

MAIL_HOST = env("MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(env("MAIL_PORT", "587"))
MAIL_USERNAME = env("MAIL_USERNAME")
MAIL_PASSWORD = env("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = env("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

FLASK_HOST = env("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(env("FLASK_PORT", "5000"))
FLASK_DEBUG = env("FLASK_DEBUG", "1") == "1"
BACKEND_BASE_URL = env("BACKEND_BASE_URL", "http://127.0.0.1:5000")
FRONTEND_BASE_URL = env("FRONTEND_BASE_URL",  "http://localhost:3000")