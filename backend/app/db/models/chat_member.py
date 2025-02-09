"""
Chat model for group chats with AI.
"""

import enum

from sqlalchemy import UUID, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class ChatMemberStatus(enum.Enum):
    """Enum for chat member status."""

    JOIN_REQUEST = "join_request"
    MEMBER = "member"
    ADMIN = "admin"
    BANNED = "banned"
    OWNER = "owner"


class ChatMember(Base):
    """
    Database model for chat memberswith their roles.
    """

    __tablename__ = "chat_members"

    chat_id = Column(UUID, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)

    status = Column(
        Enum(ChatMemberStatus), default=ChatMemberStatus.JOIN_REQUEST, nullable=False
    )

    chat = relationship("Chat", back_populates="members")
    # user = relationship("User", back_populates="chat_memberships")
