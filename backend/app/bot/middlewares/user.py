"""
Middleware for handling user-related operations in the Telegram bot.
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class UserMiddleware(BaseMiddleware):
    """
    Middleware to process and manage user-related context in bot interactions.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user
        repos = data["db_repos"]

        db_user = await repos.user_repo.create_or_update_user(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

        data["user"] = db_user
        return await handler(event, data)
