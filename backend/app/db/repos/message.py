"""
Message repository module for managing message-related database operations.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repos.base import BaseRepository
from backend.app.db.models.chat_message import ChatMessage, MessageSource


class MessageRepository(BaseRepository):
    """
    Repository for managing message-related database operations.
    """

    async def create_message(
        self, chat_id: UUID, user_id: UUID, content: str
    ) -> ChatMessage:
        """
        Create a new message.

        :param chat_id: The ID of the chat
        :param user_id: The ID of the user sending the message
        :param content: The message content
        :return: The created message
        """
        try:
            message = ChatMessage(
                chat_id=chat_id,
                user_id=user_id,
                content=content,
            )
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            return message
        except IntegrityError:
            await self.db.rollback()
            raise

    async def get_messages_by_chat(
        self, chat_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[ChatMessage]:
        """
        Retrieve messages for a specific chat.

        :param chat_id: The ID of the chat
        :param limit: Maximum number of messages to retrieve
        :param offset: Number of messages to skip
        :return: List of messages
        """
        query = (
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_message_by_id(self, message_id: UUID) -> Optional[ChatMessage]:
        """
        Retrieve a specific message by its ID.

        :param message_id: The ID of the message
        :return: The message if found, None otherwise
        """
        query = select(ChatMessage).where(ChatMessage.id == message_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete_message(self, message_id: UUID) -> bool:
        """
        Delete a specific message.

        :param message_id: The ID of the message to delete
        :return: True if the message was deleted, False otherwise
        """
        message = await self.get_message_by_id(message_id)
        if not message:
            return False

        await self.db.delete(message)
        await self.db.commit()
        return True
