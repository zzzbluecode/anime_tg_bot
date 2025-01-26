from typing import Optional

from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from src.constant.constant import (
    STATE_ANIME_NAME,
)
from src.keyboard.keyboard import (
    get_core_function_keyboard,
)

import logging
logger = logging.getLogger("tg_bot")

class AddAnimeFeatureHandler:
    """Handler for /add_anime command."""
    
    def __init__(self, bot):
        self.bot = bot

    async def add_anime_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handler for adding an anime.
        
        Args:
            update: Telegram update object
            context: Callback context
            
        Returns:
            Next conversation state
        """
        if not await self.bot.check_user_permission(update):
            return ConversationHandler.END

        user = update.effective_user
        logger.info(f"User {user.username} (ID: {user.id}): add anime command")
        
        await update.message.reply_text(
            "Please enter the name of the anime you want to add:",
            reply_markup=None
        )
        logger.info(f"Bot: waiting User {user.username} (ID: {user.id}) to input anime name")
        return STATE_ANIME_NAME

    async def add_anime_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle the anime name input.
        
        Args:
            update: Telegram update object
            context: Callback context
            
        Returns:
            End of conversation
        """
        if not await self.bot.check_user_permission(update):
            return ConversationHandler.END
            
        user = update.effective_user
        anime_name = update.message.text
        self.bot.anime_manager.add_anime(anime_name)
        logger.info(f"User {user.username} (ID: {user.id}): added anime: {anime_name}")
        
        await update.message.reply_text(
            f"Added {anime_name} to your list! 🎉\n"
            f"\n"
            f"Use /add_anime to add more anime\n"
            f"\n"
            f"Use /get_animes to view your list",
            reply_markup=get_core_function_keyboard()
        )
        logger.info(f"Bot: confirmed adding '{anime_name}' to User {user.username} (ID: {user.id})")
        return ConversationHandler.END
