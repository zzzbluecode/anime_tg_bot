from telegram import Update
from telegram.ext import ContextTypes
from src.constant.constant import WELCOME_MESSAGE
from src.keyboard.keyboard import get_core_function_keyboard

import logging
logger = logging.getLogger("tg_bot")

class StartFeatureHandler:
    """Handler for /start command."""
    
    def __init__(self, bot):
        """Initialize the handler with the bot instance."""
        self.bot = bot

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler for /start command.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        if not await self.bot.check_user_permission(update):
            return

        user = update.effective_user
        logger.info(f"User {user.username} (ID: {user.id}): start command")
        
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=get_core_function_keyboard()
        )
        logger.info(f"Bot: sent welcome message to User {user.username} (ID: {user.id})")
