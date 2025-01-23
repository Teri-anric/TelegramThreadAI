"""
Chat member repository module for managing chat member-related database operations.

This module provides functionality to create, update, and retrieve
chat member information, handling various statuses and interactions
within chat groups.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.db.models.chat_member import ChatMember, ChatMemberStatus
from app.db.repos.base import BaseRepository


class ChatMemberRepository(BaseRepository):
    """
    Chat member repository for managing chat member-related database operations.
    """

    # ### Creators ###

    async def create_chat_member(
        self, chat_id: UUID, user_id: UUID, status: ChatMemberStatus
    ) -> bool:
        """
        Create a chat member.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :param status: The status of the chat member.
        :return: True if the chat member was created successfully, False otherwise.
        """
        try:
            chat_member = ChatMember(chat_id=chat_id, user_id=user_id, status=status)
            self.db.add(chat_member)
            await self.db.commit()
            return True
        except IntegrityError:
            return False

    async def change_chat_member_status(
        self,
        chat_id: UUID,
        user_id: UUID,
        old_status: List[ChatMemberStatus] | ChatMemberStatus,
        new_status: ChatMemberStatus,
    ) -> bool:
        """
        Change the status of a chat member.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :param old_status: The current status(es) of the chat member.
        :param new_status: The new status to set.
        :return: True if the status was changed successfully, False otherwise.
        """
        if not isinstance(old_status, list):
            old_status = [old_status]

        result = await self.db.execute(
            update(ChatMember)
            .where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id,
                ChatMember.status.in_(old_status),
            )
            .values(status=new_status)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def send_join_request(self, chat_id: UUID, user_id: UUID) -> bool:
        """
        Send a join request to a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: True if the join request was sent successfully, False otherwise.
        """
        return await self.create_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            status=ChatMemberStatus.JOIN_REQUEST,
        )

    async def accept_join_request(self, chat_id: UUID, user_id: UUID) -> bool:
        """
        Accept a join request to a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: True if the join request was accepted successfully, False otherwise.
        """
        return await self.change_chat_member_status(
            chat_id=chat_id,
            user_id=user_id,
            old_status=ChatMemberStatus.JOIN_REQUEST,
            new_status=ChatMemberStatus.MEMBER,
        )

    async def reject_join_request(self, chat_id: UUID, user_id: UUID) -> bool:
        """
        Reject a join request to a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: True if the join request was rejected successfully, False otherwise.
        """
        return await self.change_chat_member_status(
            chat_id=chat_id,
            user_id=user_id,
            old_status=ChatMemberStatus.JOIN_REQUEST,
            new_status=ChatMemberStatus.BANNED,
        )

    async def promote_to_admin(self, chat_id: UUID, user_id: UUID) -> bool:
        """
        Promote a member to admin.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: True if the member was promoted successfully, False otherwise.
        """
        return await self.change_chat_member_status(
            chat_id=chat_id,
            user_id=user_id,
            old_status=ChatMemberStatus.MEMBER,
            new_status=ChatMemberStatus.ADMIN,
        )

    async def add_to_chat(
        self, chat_id: UUID, user_id: UUID, is_admin: bool = False
    ) -> bool:
        """
        Add a user to a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :param is_admin: Whether the user should be added as an admin.
        :return: True if the user was added successfully, False otherwise.
        """
        status = ChatMemberStatus.MEMBER
        if is_admin:
            status = ChatMemberStatus.ADMIN

        return await self.create_chat_member(
            chat_id=chat_id, user_id=user_id, status=status
        )

    async def remove_from_chat(self, chat_id: UUID, user_id: UUID) -> bool:
        """
        Remove a user from a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: True if the user was removed successfully, False otherwise.
        """
        return await self.change_chat_member_status(
            chat_id=chat_id,
            user_id=user_id,
            old_status=[ChatMemberStatus.MEMBER, ChatMemberStatus.ADMIN],
            new_status=ChatMemberStatus.BANNED,
        )

    # ### Getters ###

    async def get_chat_member(
        self, chat_id: UUID, user_id: UUID
    ) -> Optional[ChatMember]:
        """
        Get a chat member, user in a chat.

        :param chat_id: The ID of the chat.
        :param user_id: The ID of the user.
        :return: The chat member if found, None otherwise.
        """
        result = await self.db.execute(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id, ChatMember.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_chat_members_by_status(
        self, chat_id: UUID, status: ChatMemberStatus
    ) -> List[ChatMember]:
        """
        Get chat members by status.

        :param chat_id: The ID of the chat.
        :param status: The status of the chat members to retrieve.
        :return: A list of chat members with the specified status.
        """
        result = await self.db.execute(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id, ChatMember.status == status
            )
        )
        return result.scalars().all()

    async def get_chat_members(self, chat_id: UUID) -> List[ChatMember]:
        """
        Get chat members.

        :param chat_id: The ID of the chat.
        :return: A list of chat members.
        """
        return await self.get_chat_members_by_status(chat_id, ChatMemberStatus.MEMBER)

    async def get_chat_admins(self, chat_id: UUID) -> List[ChatMember]:
        """
        Get chat admins.

        :param chat_id: The ID of the chat.
        :return: A list of chat admins.
        """
        return await self.get_chat_members_by_status(chat_id, ChatMemberStatus.ADMIN)

    async def get_chat_join_requests(self, chat_id: UUID) -> List[ChatMember]:
        """
        Get chat join requests.

        :param chat_id: The ID of the chat.
        :return: A list of chat join requests.
        """
        return await self.get_chat_members_by_status(
            chat_id, ChatMemberStatus.JOIN_REQUEST
        )

    async def get_chat_banned_members(self, chat_id: UUID) -> List[ChatMember]:
        """
        Get chat banned members.

        :param chat_id: The ID of the chat.
        :return: A list of banned chat members.
        """
        return await self.get_chat_members_by_status(chat_id, ChatMemberStatus.BANNED)
