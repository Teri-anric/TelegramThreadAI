"""
Handlers for incoming messages from users.
"""

from aiogram import Router
from aiogram.types import Message

from app.bot.middlewares.context import DBReposContext
from app.db.models.user import User
from app.services.message_queue import MessageQueueService

router = Router()


@router.message()
async def echo_message(
    message: Message,
    user: User,
    db_repos: DBReposContext,
    mq_service: MessageQueueService,
):
    """
    Process an incoming message from a user.

    Args:
        message (Message): The incoming Telegram message.
    """
    chat = await db_repos.chat_repo.get_chat_by_telegram_id(message.chat.id)

    if chat:
        await mq_service.publish_message(
            chat_id=chat.id, user_id=user.id, content=message.text
        )
