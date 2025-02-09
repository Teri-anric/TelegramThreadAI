"""
Message model for storing chat messages.
"""

import uuid

from sqlalchemy import UUID, Column, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class ChatMessage(Base):
    """
    Database model for storing chat messages.
    """

    __tablename__ = "chat_messages"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    chat_id = Column(
        UUID,
        ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        UUID,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    content = Column(Text, nullable=False)

    # timestamps realted in base model

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    user = relationship("User")
