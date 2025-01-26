from telegram import (
    Update,
    User
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from src.constant.constant import (
    STATE_EDIT_DESCRIPTION,
    STATE_EDIT_EPISODE,
)
from src.keyboard.keyboard import (
    get_core_function_keyboard,
    get_anime_details_keyboard,
    get_rating_keyboard,
    get_status_keyboard,
    get_episode_editor_keyboard,
    get_anime_list_keyboard,
    get_view_detail_keyboard
)

import logging
logger = logging.getLogger("tg_bot")

class GetAnimesFeatureHandler:
    """Handler for /get_animes command."""
    
    def __init__(self, bot):
        self.bot = bot

    async def get_animes_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handler for retrieving animes.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        if not await self.bot.check_user_permission(update):
            return

        user = update.effective_user
        logger.info(f"User {user.username} (ID: {user.id}): get animes command")
        
        animes = self.bot.anime_manager.get_all_animes()
        if not animes:
            await update.message.reply_text(
                "No animes found in the database.",
                reply_markup=get_core_function_keyboard()
            )
            logger.info(f"Bot: informed User {user.username} (ID: {user.id}) that no animes were found")
            return

        logger.info(f"Bot: showing anime list ({len(animes)} items) to User {user.username} (ID: {user.id})")
        await update.message.reply_text(
            "Here are your animes:",
            reply_markup=get_anime_list_keyboard(animes)
        )

    async def get_animes(self, update: Update, user: User) -> None:
        """
        Handler for retrieving animes.
        
        Args:
            update: Telegram update object
            user: User
        """
        logger.info(f"User {user.username} (ID: {user.id}): get animes command")
        
        animes = self.bot.anime_manager.get_all_animes()
        if not animes:
            await update.message.reply_text(
                "No animes found in the database.",
                reply_markup=get_core_function_keyboard()
            )
            logger.info(f"Bot: informed User {user.username} (ID: {user.id}) that no animes were found")
            return

        logger.info(f"Bot: showing anime list ({len(animes)} items) to User {user.username} (ID: {user.id})")
        await update.message.reply_text(
            "Here are your animes:",
            reply_markup=get_anime_list_keyboard(animes)
        )

    async def show_anime_details(self, query: Update.callback_query) -> None:
        """
        Show details for a specific anime.
        
        Args:
            query: Callback query
            index: Index of the anime to show
        """
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) opened anime details")
        index = int(query.data.split(',')[-1])
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if not anime:
            logger.info(f"Bot: anime {index} not found to User {query.from_user.username} (ID: {query.from_user.id})") 
            return
            
        details_text = (
            f"📺 Anime: {anime.name}\n"
            f"📝 Description: {anime.description or 'Not set'}\n"
            f"⭐ Rating: {'⭐' * int(anime.rating) if anime.rating else 'Not rated'}\n"
            f"📊 Status: {anime.status}\n"
            f"🎬 Episodes: {anime.episodes}"
        )
        
        await query.edit_message_text(
            details_text,
            reply_markup=get_anime_details_keyboard(index)
        )
        logger.info(f"Bot: showing details of '{anime.name}' to User {query.from_user.username} (ID: {query.from_user.id})")

    async def show_episode_editor(self, query: Update.callback_query, index: int) -> None:
        """
        Show episode editor for a specific anime.
        
        Args:
            query: Callback query
            index: Index of the anime to edit
        """
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) opened episode editor")
        
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if not anime:
            logging.warning(f"Anime with index {index} not found")
            return
        
        logger.info(f"Bot: showing episode editor for '{anime.name}' to User {query.from_user.username} (ID: {query.from_user.id})")
        await query.edit_message_text(
            f"Edit episodes for {anime.name}:",
            reply_markup=get_episode_editor_keyboard(index, anime.episodes)
        )
        logger.info(f"Bot: waiting for user response on episode editor for {anime.name}")

    async def show_description_editor(self, query: Update.callback_query, user: User) -> None:
        """
        Show description editor for a specific anime.
        
        Args:
            query: Callback query
            user: User object
        """
        logger.info(f"User {user.username} (ID: {user.id}) initiated edit of description")
        
        await query.edit_message_text(
            "Please enter a new description for the anime:",
            reply_markup=None
        )
        logger.info(f"Bot: waiting User {user.username} (ID: {user.id}) to input new description")
        return STATE_EDIT_DESCRIPTION

    async def show_rating_editor(self, query: Update.callback_query, index: int) -> None:
        """
        Show rating editor for a specific anime.
        
        Args:
            query: Callback query
            index: Index of the anime to edit
        """
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) opened rating editor")
        
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if not anime:
            logging.warning(f"Anime with index {index} not found")
            return

        logger.info(f"Bot: showing rating editor for '{anime.name}' to User {query.from_user.username} (ID: {query.from_user.id})")
        await query.edit_message_text(
            "Select a rating for the anime:",
            reply_markup=get_rating_keyboard(index)
        )
        logger.info(f"Bot: waiting for user response on rating editor for {anime.name}")

    async def show_status_editor(self, query: Update.callback_query, index: int) -> None:
        """
        Show status editor for a specific anime.
        
        Args:
            query: Callback query
            index: Index of the anime to edit
        """
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) opened status editor")
        
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if not anime:
            logging.warning(f"Anime with index {index} not found")
            return

        logger.info(f"Bot: showing status editor for '{anime.name}' to User {query.from_user.username} (ID: {query.from_user.id})")
        await query.edit_message_text(
            "Select the status for the anime:",
            reply_markup=get_status_keyboard(index)
        )
        logger.info(f"Bot: waiting for user response on status editor for {anime.name}")

    async def handle_description_edit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle the description edit input.
        
        Args:
            update: Telegram update object
            context: Callback context
            
        Returns:
            End of conversation
        """
        if not await self.bot.check_user_permission(update):
            return ConversationHandler.END
            
        user = update.effective_user
        anime_name = self.bot.current_edit[user.id]['anime_name']
        index = self.bot.current_edit[user.id]['index']
        new_description = update.message.text
        
        self.bot.anime_manager.update_anime(anime_name, description=new_description)
        logger.info(f"User {user.username} (ID: {user.id}): updated description for {anime_name}")
        
        # Show success message with inline keyboard to view details
        await update.message.reply_text(
            f"Description updated for {anime_name}! 📝",
            reply_markup=get_view_detail_keyboard(index)
        )
        logger.info(f"Bot: confirmed description update for '{anime_name}' to User {user.username} (ID: {user.id})")
        return ConversationHandler.END

    async def edit_episode(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Handle the episode edit input.
        
        Args:
            update: Telegram update object
            context: Callback context
            
        Returns:
            End of conversation
        """
        if not await self.bot.check_user_permission(update):
            return ConversationHandler.END
            
        user = update.effective_user
        anime_name = self.bot.current_edit[user.id]['anime_name']
        index = self.bot.current_edit[user.id]['index']
        
        try:
            new_episodes = int(update.message.text)
            if new_episodes < 0:
                raise ValueError("Episodes cannot be negative")
                
            self.bot.anime_manager.update_anime(anime_name, episodes=new_episodes)
            logger.info(f"User {user.username} (ID: {user.id}): set episodes for {anime_name} to {new_episodes}")
            
            # Show success message with inline keyboard to view details
            await update.message.reply_text(
                f"Episodes updated for {anime_name}! 🎬",
                reply_markup=get_view_detail_keyboard(index)
            )
            
            logger.info(f"Bot: confirmed episode update for '{anime_name}' to User {user.username} (ID: {user.id})")
            return ConversationHandler.END
            
        except ValueError as e:
            await update.message.reply_text(
                "Please enter a valid positive number for episodes:",
                reply_markup=None
            )
            logger.info(f"Bot: informed User {user.username} (ID: {user.id}) about invalid episode number")
            logger.info(f"Bot: waiting User {user.username} (ID: {user.id}) to input valid episode number")
            return STATE_EDIT_EPISODE

    async def show_episode_number_editor(self, query: Update.callback_query, index: int, anime_name: str) -> None:
        """
        Show episode number editor for a specific anime.
        
        Args:
            query: Callback query
            anime_name: Anime name
        """
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) initiated manual episode set for {anime_name}")
        self.bot.current_edit[query.from_user.id] = {
            'anime_name': anime_name,
            'edit_type': 'episode',
            'index': index  # Store index for returning to details view
        }
        await query.edit_message_text(
            f"Please enter the episode number for {anime_name}:",
            reply_markup=None
        )
        logger.info(f"Bot: waiting User {query.from_user.username} (ID: {query.from_user.id}) to input episode number")
        return STATE_EDIT_EPISODE

    async def handle_episode_button_callback(self, query: Update.callback_query) -> None:
        logger.info(f"handle_episode_button_callback start")
        logging.debug(f"query {query}")
        _, action, index = query.data.split(',')
        index = int(index)
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if anime:
            current_episodes = anime.episodes
            
            if action == 'plus':
                self.bot.anime_manager.update_anime(anime.name, episodes=current_episodes + 1)
                logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): incremented episode count for {anime.name} to {current_episodes + 1}")
                await self.show_episode_editor(query, index)
            elif action == 'minus':
                if current_episodes > 0:
                    self.bot.anime_manager.update_anime(anime.name, episodes=current_episodes - 1)
                    logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): decremented episode count for {anime.name} to {current_episodes - 1}")
                    await self.show_episode_editor(query, index)
            elif action == 'set':
                logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}) initiated manual episode set for {anime.name}")
                return await self.show_episode_number_editor(query, index, anime.name)
            elif action == 'back':
                await self.show_anime_details(query)

    async def handle_anime_edit_button_callback(self, query: Update.callback_query) -> None:
        logger.info(f"handle_anime_edit_button_callback start")
        _, edit_type, index = query.data.split(',')
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): initiated edit of {edit_type} for index: {index}")
        if edit_type == 'get_animes':
            return await self.bot.get_animes_handler.get_animes(query, query.from_user)

        index = int(index)
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if anime:
            logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): initiated edit of {edit_type} for anime: {anime.name}")
            self.bot.current_edit[query.from_user.id] = {
                'anime_name': anime.name,
                'edit_type': edit_type,
                'index': index  # Store index for returning to details view
            }
            
            if edit_type == 'desc':
                return await self.show_description_editor(query, query.from_user)
            elif edit_type == 'episode':
                return await self.show_episode_editor(query, index)
            elif edit_type == 'rating':
                return await self.show_rating_editor(query, index)
            elif edit_type == 'status':
                return await self.show_status_editor(query, index)

    async def handle_status_button_callback(self, query: Update.callback_query) -> None:
        _, value, index = query.data.split(',')
        index = int(index)
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if anime:
            self.bot.anime_manager.update_anime(anime.name, status=value)
            logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): set status to {value} for {anime.name}")
            await self.show_anime_details(query)

    async def handle_rating_button_callback(self, query: Update.callback_query) -> None:
        _, value, index = query.data.split(',')
        index = int(index)
        anime = self.bot.anime_manager.get_anime_by_index(index)
        if anime:
            self.bot.anime_manager.update_anime(anime.name, rating=value)
            logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): set rating to {value} for {anime.name}")
            await self.show_anime_details(query)
