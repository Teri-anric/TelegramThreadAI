"""
Main entry point for the Telegram bot application before testing.
"""

from .core import bot, dp

if __name__ == "__main__":
    assert (
        bot is not None
    ), "Bot is not initialized, check environment variable BOT_TOKEN"
    dp.run_polling(bot)
