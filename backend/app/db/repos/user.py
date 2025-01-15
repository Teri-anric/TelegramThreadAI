"""
User repository module.
"""

from typing import Optional

from sqlalchemy.future import select

from ..models import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    """
    User repository (CRUD operations for the user models).
    """

    async def create_user(
        self,
        telegram_id: int,
        first_name: str = None,
        last_name: str = None,
        username: str = None,
        photo_url: str = None,
    ) -> User:
        """
        Create a new user in the database
        """
        new_user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            photo_url=photo_url,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def create_or_update_user(
        self,
        telegram_id: int,
        first_name: str = None,
        last_name: str = None,
        username: str = None,
        photo_url: str = None,
    ) -> User:
        """
        Create or update a user in the database
        """
        existing_user = await self.get_user_by_telegram_id(telegram_id)

        if existing_user:
            # Update existing user
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.username = username
            existing_user.photo_url = photo_url
            await self.db.commit()
            await self.db.refresh(existing_user)
            return existing_user

        return await self.create_user(
            telegram_id, first_name, last_name, username, photo_url
        )

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get a user by Telegram ID
        """
        result = await self.db.execute(
            select(User).filter(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by internal ID
        """
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
