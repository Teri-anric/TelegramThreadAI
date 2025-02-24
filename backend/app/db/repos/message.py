"""
Message repository module for managing message-related database operations.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.db.models.chat_message import ChatMessage
from app.db.repos.base import BaseRepository
from app.db.types.pagination import Pagination


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
        self, chat_id: UUID, page: int = 1, per_page: int = 50
    ) -> Pagination[ChatMessage]:
        """
        Retrieve paginated messages for a specific chat.

        :param chat_id: The ID of the chat
        :param page: Page number for pagination
        :param per_page: Number of messages per page
        :return: Paginated messages with total count
        """
        query = (
            select(ChatMessage)
            .options(joinedload(ChatMessage.user))
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_at.desc())
        )
        return await Pagination.from_query(
            self.db,
            query=query,
            page=page,
            per_page=per_page
        )

    async def get_message_by_id(self, message_id: UUID) -> Optional[ChatMessage]:
        """
        Retrieve a message by its ID.

        :param message_id: The ID of the message
        :return: The message if found, None otherwise
        """
        result = await self.db.execute(select(ChatMessage).where(ChatMessage.id == message_id))
        return result.scalar_one_or_none()

    async def delete_message(self, message_id: UUID) -> bool:
        """
        Delete a specific message.

        :param message_id: The ID of the message to delete
        :return: True if the message was deleted, False otherwise
        """
        result = await self.db.execute(delete(ChatMessage).where(ChatMessage.id == message_id))
        return result.rowcount > 0
