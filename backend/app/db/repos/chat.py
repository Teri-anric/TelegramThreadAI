"""
Chat repository module for managing chat-related database operations.
"""

from contextlib import suppress
import secrets
from typing import Optional
from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.db.models.chat import Chat, ChatType
from app.db.models.chat_member import ChatMember, ChatMemberStatus
from app.db.repos.base import BaseRepository
from app.db.repos.exptions import ChatUsernameAlreadyExistsException


class ChatRepository(BaseRepository):
    """
    Chat repository for managing chat-related database operations.
    """

    async def get_chat_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """
        Get a chat by its ID.

        :param chat_id: The ID of the chat.
        :return: The chat if found, None otherwise.
        """
        result = await self.db.execute(
            select(Chat).where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def get_chat_by_username(self, username: str) -> Optional[Chat]:
        """
        Get a chat by its username.

        :param username: The username of the chat.
        :return: The chat if found, None otherwise.
        """
        result = await self.db.execute(
            select(Chat)
            .where(Chat.username == username)
        )
        return result.scalar_one_or_none()

    async def create_chat(
        self,
        owner_id: UUID,
        title: str,
        username: str = None,
        description: Optional[str] = None,
        avatar_url: Optional[str] = None,
        chat_type: ChatType = ChatType.PRIVATE,
    ) -> Chat:
        """
        Create a new chat.

        :param owner_id: The ID of the chat owner.
        :param title: The title of the chat.
        :param username: The username of the chat (optional, if not provided, a random one will be generated).
        :param description: The description of the chat (optional).
        :param avatar_url: The avatar URL of the chat (optional).
        :param chat_type: The type of the chat (default is PRIVATE).

        :return: The created chat.
        """
        if not username:
            username = secrets.token_urlsafe(10)

        new_chat = Chat(
            title=title,
            username=username,
            description=description,
            avatar_url=avatar_url,
            chat_type=chat_type,
            owner_id=owner_id,
        )

        try:
            self.db.add(new_chat)
            await self.db.commit()
            await self.db.refresh(new_chat)
        except IntegrityError:
            await self.db.rollback()
            raise ChatUsernameAlreadyExistsException()
        
        owner_chat_member = ChatMember(
            chat_id=new_chat.id, user_id=owner_id, status=ChatMemberStatus.OWNER
        )
        self.db.add(owner_chat_member)
        await self.db.commit()

        return new_chat
    

    async def update_chat(
        self,
        chat_id: UUID,
        title: str,
        username: str,
        description: str,
        chat_type: ChatType,
    ) -> bool:
        """
        Update a chat.

        :param chat_id: The ID of the chat to update.
        :param title: The new title of the chat.
        :param username: The new username of the chat.
        :param description: The new description of the chat.
        :param chat_type: The new type of the chat.

        :return: True if the chat was updated successfully, False otherwise.
        """
        with suppress(IntegrityError):
            result = await self.db.execute(
                update(Chat)
                .where(Chat.id == chat_id)
                .values(
                    title=title,
                    description=description,
                    username=username,
                    chat_type=chat_type,
                )
            )
            await self.db.commit()
            return result.rowcount > 0
        raise ChatUsernameAlreadyExistsException()

    async def update_chat_avatar(self, chat_id: UUID, avatar_url: str) -> bool:
        """
        Update a chat avatar.

        :param chat_id: The ID of the chat.
        :param avatar_url: The new avatar URL.
        
        :return: True if the avatar was updated successfully, False otherwise.
        """
        result = await self.db.execute(
            update(Chat).where(Chat.id == chat_id).values(avatar_url=avatar_url)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def delete_chat(self, chat_id: UUID) -> bool:
        """
        Delete a chat.

        :param chat_id: The ID of the chat to delete.
        :return: True if the chat was deleted successfully, False otherwise.
        """
        result = await self.db.execute(delete(Chat).where(Chat.id == chat_id))
        await self.db.commit()
        return result.rowcount > 0
