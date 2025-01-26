from typing import Optional, Dict, Callable, List
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
import logging

logger = logging.getLogger("tg_bot")

class ButtonCallbackManager:
    def __init__(self, bot):
        self.bot = bot
        self.callbacks: Dict[Optional[str], Callable] = {}
        self.callback_query_handler: Dict[Optional[str], Callable] = {}

    def register_callback(self, callback: Callable, pattern: Optional[str] = None) -> None:
        """Register a callback for buttons matching a specific pattern.
        
        Args:
            callback: The callback function to be executed.
            pattern: The pattern to match for the callback. If None, it acts as a fallback.
        """
        self.callbacks[pattern] = callback

    def get_callback_query_handlers(self) -> List[CallbackQueryHandler]:
        """Generate a list of CallbackQueryHandler instances for registered callbacks.
        
        Returns:
            List[CallbackQueryHandler]: A list of handlers for the registered callbacks.
        """
        callback_query_handlers = []
        none_pattern_handler = None

        for pattern, callback in self.callbacks.items():
            handler = self.get_callback_query_handler(pattern)
            if pattern is not None:
                callback_query_handlers.append(CallbackQueryHandler(handler, pattern=pattern))
            else:
                none_pattern_handler = CallbackQueryHandler(handler)

        # Place the None pattern handler at the end
        if none_pattern_handler is not None:
            callback_query_handlers.append(none_pattern_handler)

        return callback_query_handlers

    def get_callback_query_handler(self, pattern: Optional[str]) -> Callable:
        """Get or create a callback handler for a specific pattern.
        
        Args:
            pattern: The pattern to get the handler for.
        
        Returns:
            Callable: The callback handler function.
        """
        if pattern not in self.callback_query_handler:
            callback = self.callbacks[pattern]

            async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[str]:
                """Callback handler for inline buttons.
                
                Args:
                    update: The update object from Telegram.
                    context: The context object from Telegram.
                
                Returns:
                    Optional[str]: The result of the callback function.
                """
                if not await self.bot.check_user_permission(update):
                    return

                query = update.callback_query
                user = query.from_user
                logger.info(f"User {user.username} (ID: {user.id}): Button callback triggered, data: {query.data}")
                await query.answer()

                try:
                    res = await callback(query)
                    logger.info(f'Callback returned result: {res}')
                    return res
                except Exception as e:
                    logger.error(f"Error executing callback for pattern {pattern}: {e}", exc_info=True)
                    await query.answer("An error occurred. Please try again later.", show_alert=True)

            logger.debug(f"Registered button_callback for pattern: {pattern}")
            self.callback_query_handler[pattern] = button_callback

        logger.debug(f"Retrieved button_callback for pattern: {pattern}")
        return self.callback_query_handler[pattern]