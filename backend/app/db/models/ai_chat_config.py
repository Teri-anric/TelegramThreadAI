"""
AI Configuration model for group chats.
"""

from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AIChatConfig(Base):
    """
    Database model for AI configuration for group/chats.
    """

    __tablename__ = "ai_chat_configs"

    chat_id = Column(UUID, ForeignKey("chats.id"), primary_key=True)
    prompt = Column(String, nullable=False)
    model = Column(String, nullable=False)

    trigger_on_message_count = Column(Boolean, default=False, nullable=False)
    message_count_threshold = Column(Integer, default=10, nullable=False)

    trigger_on_time_interval = Column(Boolean, default=False, nullable=False)
    time_interval_seconds = Column(Integer, default=60, nullable=False)

    trigger_on_mention = Column(Boolean, default=False, nullable=False)

    # max_messages_per_interval = Column(Integer, default=10, nullable=False)

    chat = relationship("Chat", back_populates="ai_config", uselist=False)
