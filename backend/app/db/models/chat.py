"""
Chat model for group chats with AI.
"""

import enum
import uuid

from sqlalchemy import UUID, Column, Enum, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class ChatType(enum.Enum):
    """Enum for chat types."""

    PUBLIC = "public"
    PRIVATE = "private"
    TELEGRAM = "mirrored_telegram"


class Chat(Base):
    """
    Database model for group/chats.
    """

    __tablename__ = "chats"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    chat_type = Column(Enum(ChatType), default=ChatType.PUBLIC, nullable=False)
    owner_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    telegram_chat_id = Column(BigInteger, nullable=True, index=True)

    owner = relationship("User", back_populates="owned_chats")
    members = relationship("ChatMember", back_populates="chat")
    # chat_permissions = relationship("ChatPermission", back_populates="chat", uselist=False)

    ai_config = relationship(
        "AIChatConfig",
        back_populates="chat",
        uselist=False,
        cascade="all, delete-orphan",
    )

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
