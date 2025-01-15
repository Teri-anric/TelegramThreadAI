"""
Configuration file.
"""

import os
import secrets

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database configuration
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
).render_as_string(hide_password=False)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
ALGORITHM = os.getenv("ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24 * 7
)  # 7 days
