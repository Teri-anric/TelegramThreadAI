from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "🚀 Welcome to TelegramThreadAI!\n\n"
        "I'll help you manage AI-enhanced group conversations. "
        "Create or join chats to start interacting!"
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""
    /start - Start the bot
    """)
