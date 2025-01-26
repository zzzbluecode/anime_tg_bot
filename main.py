"""Main entry point for the Telegram bot application."""

from src.log.logging_config import setup_root_logging, setup_logging
from src.bot.telegram_bot import TelegramBot

if __name__ == '__main__':
    setup_root_logging()
    setup_logging("tg_bot")

    bot = TelegramBot()
    bot.run()
