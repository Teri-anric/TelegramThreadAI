"""
Core module for Telegram bot initialization and configuration.
"""

from logging import getLogger

from aiogram import Bot, Dispatcher
from aiogram.utils.token import TokenValidationError

from app.config import settings
from app.services.message_queue import MessageQueueService

from .handlers import index_router
from .middlewares import DatabaseMiddleware, UserMiddleware

logger = getLogger(__name__)

bot: Bot | None = None
try:
    bot = Bot(token=settings.bot_token)
except TokenValidationError:
    logger.warning(
        "BOT_TOKEN is not set or invalid, all telegram bot functions will be disabled"
    )

dp = Dispatcher()

# Setup middleware
dp.update.middleware(DatabaseMiddleware())
dp.message.middleware(UserMiddleware())

dp["mq_service"] = MessageQueueService()

dp.include_router(index_router)
