from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

from src.config.config import Config
from src.constant.constant import (
    STATE_ANIME_NAME,
    STATE_EDIT_DESCRIPTION,
    STATE_EDIT_EPISODE,
    UNAUTHORIZED_MESSAGE,
)
from src.model.anime import AnimeDetailsManager
from src.keyboard.keyboard import (
    get_core_function_keyboard,
)

from src.functionality.StartFeature.StartFeatureHandler import StartFeatureHandler
from src.functionality.AddAnimeFeature.AddAnimeFeatureHandler import AddAnimeFeatureHandler
from src.functionality.GetAnimesFeature.GetAnimesFeatureHandler import GetAnimesFeatureHandler
from src.functionality.HelpFeature.HelpFeatureHandler import HelpFeatureHandler
from src.manager.ButtonCallbackManager import ButtonCallbackManager

import logging
logger = logging.getLogger("tg_bot")

class TelegramBot:
    """Main Telegram bot class for anime management."""
    
    def __init__(self):
        """Initialize the bot with configuration and managers."""
        logger.info("Initializing TelegramBot")
        self.config = Config()
        self.anime_manager = AnimeDetailsManager()
        self.current_edit = {}
        self.button_callback_manager = ButtonCallbackManager(self)
        
        self.start_handler = StartFeatureHandler(self)
        self.add_anime_handler = AddAnimeFeatureHandler(self)
        self.get_animes_handler = GetAnimesFeatureHandler(self)
        self.help_handler = HelpFeatureHandler(self)
        logger.info("TelegramBot initialization completed")

    async def check_user_permission(self, update: Update) -> bool:
        """
        Check if user is allowed to use the bot.
        
        Args:
            update: Telegram update object
            
        Returns:
            True if user is allowed, False otherwise
        """
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        if not self.config.enable_restriction:
            logger.debug(f"User {username} (ID: {user_id}) granted access - restrictions disabled")
            return True
            
        if user_id not in self.config.allowed_users:
            logging.warning(f"Unauthorized access attempt by user {username} (ID: {user_id})")
            await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            return False
            
        logger.info("")
        logger.info("==============")
        logger.info(f"Authorized user {username} (ID: {user_id}) accessed the bot")
        return True

    async def anime_detail_button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Callback handler for inline buttons.
        
        Args:
            update: Telegram update object
            context: Callback context
        """
        if not await self.check_user_permission(update):
            return

        query = update.callback_query
        user = query.from_user
        logger.info(f"User {user.username} (ID: {user.id}): anime_detail_button callback, data: {query.data}")
        await query.answer()

        if query.data.startswith('anime_detail_'):
            await self.get_animes_handler.show_anime_details(query)

    async def error_button_callback(self, query: Update.callback_query) -> None:
        logger.info('PLEASE CHECK THE data as dont expect ')
        logger.info(f"User {query.from_user.username} (ID: {query.from_user.id}): error_button_callback, data: {query.data}")
        
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Cancel the current conversation.
        
        Args:
            update: Telegram update object
            context: Callback context
            
        Returns:
            End of conversation
        """
        user_id = update.effective_user.id
        if user_id in self.current_edit:
            del self.current_edit[user_id]
            
        await update.message.reply_text(
            "Operation cancelled.",
            reply_markup=get_core_function_keyboard()
        )
        return ConversationHandler.END

    def run(self) -> None:
        """Start the bot."""
        # Register button callbacks directly in the constructor
        self.button_callback_manager.register_callback(self.get_animes_handler.handle_anime_edit_button_callback, 'anime_edit')
        self.button_callback_manager.register_callback(self.get_animes_handler.handle_episode_button_callback, 'episode_edit')
        self.button_callback_manager.register_callback(self.get_animes_handler.handle_rating_button_callback, 'rating')
        self.button_callback_manager.register_callback(self.get_animes_handler.handle_status_button_callback, 'status')
        self.button_callback_manager.register_callback(self.get_animes_handler.show_anime_details, 'anime_detail')
        ## uncomment for debug
        # self.button_callback_manager.register_callback(self.error_button_callback, None)
        
        application = Application.builder().token(self.config.bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_handler.start_command))
        application.add_handler(CommandHandler("s", self.start_handler.start_command))
        application.add_handler(CommandHandler("help", self.help_handler.help_command))
        application.add_handler(CommandHandler("h", self.help_handler.help_command))
        application.add_handler(CommandHandler("get_animes", self.get_animes_handler.get_animes_command))
        
        # Add conversation handlers for adding anime and editing
        add_anime_handler = ConversationHandler(
            entry_points=[
                MessageHandler(filters.Regex("^📺 Add Anime$"), self.add_anime_handler.add_anime_command),
                CommandHandler("add_anime", self.add_anime_handler.add_anime_command)
            ],
            states={
                STATE_ANIME_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_anime_handler.add_anime_name)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel)]
        )
        application.add_handler(add_anime_handler)

        # Add conversation handler for editing anime descriptions
        logger.info("Adding anime edit handler")
        anime_edit_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.button_callback_manager.get_callback_query_handler('anime_edit'), pattern='^anime_edit,')],
            states={
                STATE_EDIT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_animes_handler.handle_description_edit)],
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                CallbackQueryHandler(self.button_callback_manager.get_callback_query_handler('anime_detail'), pattern='^anime_detail,')
            ]
        )
        application.add_handler(anime_edit_handler)

        logger.info("Adding episode edit handler")
        # Add conversation handler for editing episodes
        episode_edit_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.button_callback_manager.get_callback_query_handler('episode_edit'), pattern='^episode_edit,')],
            states={
                STATE_EDIT_EPISODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_animes_handler.edit_episode)],
            },
            fallbacks=[
                CommandHandler("cancel", self.cancel),
                CallbackQueryHandler(self.button_callback_manager.get_callback_query_handler('anime_detail'), pattern='^anime_detail,')
            ]
        )
        application.add_handler(episode_edit_handler)
        
        ### fuck
        ### must add the callback handler after the conversation handler
        ### otherwise, the conversation handler will not be triggered.....
        
        # Add CallbackQueryHandlers for patterns through the ButtonCallbackManager
        for app_callback_query_handlers in self.button_callback_manager.get_callback_query_handlers():
            application.add_handler(app_callback_query_handlers)

        # Add handler for "My Anime List" button
        application.add_handler(MessageHandler(
            filters.Regex("^📚 My Anime List$"),
            self.get_animes_handler.get_animes_command
        ))

        # Start the bot
        logger.info("Bot started successfully")
        application.run_polling()