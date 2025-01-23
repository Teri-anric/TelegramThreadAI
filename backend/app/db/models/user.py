"""
User model.
"""

import uuid

from sqlalchemy import UUID, Column, Integer, String

from app.db.models.base import Base


class User(Base):
    """
    Database user model (information about the user from Telegram).
    """

    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
