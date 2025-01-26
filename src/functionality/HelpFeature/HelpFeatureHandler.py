from telegram import Update
from telegram.ext import ContextTypes

from src.constant.constant import HELP_MESSAGE
from src.keyboard.keyboard import get_core_function_keyboard

import logging
logger = logging.getLogger("tg_bot")

class HelpFeatureHandler:
    """Handler for /help command."""
    
    def __init__(self, bot):
        self.bot = bot

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler for help command.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        if not await self.bot.check_user_permission(update):
            return

        user = update.effective_user
        logger.info(f"User {user.username} (ID: {user.id}): help command")
        
        await update.message.reply_text(
            HELP_MESSAGE,
            reply_markup=get_core_function_keyboard()
        )
        logger.info(f"Bot: sent help message to User {user.username} (ID: {user.id})")

