from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from src.constant.constant import (
    STATUS_WATCHING,
    STATUS_COMPLETED,
    STATUS_ON_HOLD,
    STATUS_DROPPED,
    STATUS_PLANNED,
    BUTTON_STATUS_WATCHING,
    BUTTON_STATUS_COMPLETED,
    BUTTON_STATUS_ON_HOLD,
    BUTTON_STATUS_DROPPED,
    BUTTON_STATUS_PLANNED,
)

import logging
logger = logging.getLogger("tg_bot")

def get_core_function_keyboard() -> ReplyKeyboardMarkup:
    """
    Create the main menu keyboard.
    
    Returns:
        ReplyKeyboardMarkup for main menu
    """
    keyboard = [
        [KeyboardButton("📺 Add Anime"), KeyboardButton("📚 My Anime List")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_anime_details_keyboard(index: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for anime details view.
    
    Args:
        index: Index of the anime
        
    Returns:
        InlineKeyboardMarkup for anime details
    """
    keyboard = [
        [
            InlineKeyboardButton("📝 Edit Description", callback_data=f'anime_edit,desc,{index}'),
            InlineKeyboardButton("🎬 Edit Episodes", callback_data=f'anime_edit,episode,{index}')
        ],
        [
            InlineKeyboardButton("⭐ Edit Rating", callback_data=f'anime_edit,rating,{index}'),
            InlineKeyboardButton("📊 Edit Status", callback_data=f'anime_edit,status,{index}')
        ],
        [
            InlineKeyboardButton("📚 Get Animes", callback_data='anime_edit,get_animes,-1')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rating_keyboard(index: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for rating selection.
    
    Args:
        index: Index of the anime
        
    Returns:
        InlineKeyboardMarkup for rating selection
    """
    keyboard = [
        [
            InlineKeyboardButton("⭐", callback_data=f'rating,1,{index}'),
            InlineKeyboardButton("⭐⭐", callback_data=f'rating,2,{index}'),
            InlineKeyboardButton("⭐⭐⭐", callback_data=f'rating,3,{index}')
        ],
        [
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data=f'rating,4,{index}'),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data=f'rating,5,{index}')
        ],
        [InlineKeyboardButton("🔙 Cancel", callback_data=f'anime_detail,{index}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_status_keyboard(index: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for status selection.
    
    Args:
        index: Index of the anime
        
    Returns:
        InlineKeyboardMarkup for status selection
    """
    keyboard = [
        [
            InlineKeyboardButton(BUTTON_STATUS_WATCHING, callback_data=f'status,{STATUS_WATCHING},{index}'),
            InlineKeyboardButton(BUTTON_STATUS_COMPLETED, callback_data=f'status,{STATUS_COMPLETED},{index}')
        ],
        [
            InlineKeyboardButton(BUTTON_STATUS_ON_HOLD, callback_data=f'status,{STATUS_ON_HOLD},{index}'),
            InlineKeyboardButton(BUTTON_STATUS_DROPPED, callback_data=f'status,{STATUS_DROPPED},{index}')
        ],
        [
            InlineKeyboardButton(BUTTON_STATUS_PLANNED, callback_data=f'status,{STATUS_PLANNED},{index}'),
            InlineKeyboardButton("🔙 Cancel", callback_data=f'anime_detail,{index}')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_episode_editor_keyboard(index: int, current_episodes: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for episode editing.
    
    Args:
        index: Index of the anime
        current_episodes: Current episode count
        
    Returns:
        InlineKeyboardMarkup for episode editing
    """
    keyboard = [
        [
            InlineKeyboardButton("➖", callback_data=f'episode_edit,minus,{index}'),
            InlineKeyboardButton(f"{current_episodes}", callback_data=f'episode_edit,set,{index}'),
            InlineKeyboardButton("➕", callback_data=f'episode_edit,plus,{index}')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data=f'episode_edit,back,{index}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_anime_list_keyboard(animes: list) -> InlineKeyboardMarkup:
    """
    Create keyboard with anime list as buttons.
    
    Args:
        animes: List of anime objects
        
    Returns:
        InlineKeyboardMarkup for anime list
    """
    keyboard = []
    for i, anime in enumerate(animes):
        # Get status emoji
        status_emoji = {
            STATUS_WATCHING: "📺",
            STATUS_COMPLETED: "✅",
            STATUS_ON_HOLD: "⏸️",
            STATUS_DROPPED: "❌",
            STATUS_PLANNED: "📝"
        }.get(anime.status, "❔")
        logger.info(f"anime.status: {anime.status}")
        logger.info(f"Status emoji: {status_emoji}")
        
        # Add rating stars if rated
        rating_str = f" {'⭐' * int(anime.rating)}" if anime.rating else ""
        
        # Add episode count if any
        episode_str = f" [{anime.episodes}]" if anime.episodes > 0 else ""
        
        # Create button text with status emoji, name, rating, and episodes
        button_text = f"{status_emoji} {anime.name}{rating_str}{episode_str}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f'anime_detail,{i}')])
    
    return InlineKeyboardMarkup(keyboard)

def get_view_detail_keyboard(index: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for viewing anime details.
    
    Args:
        index: Index of the anime
        
    Returns:
        InlineKeyboardMarkup for viewing anime details
    """
    keyboard = [[InlineKeyboardButton("View Details", callback_data=f'anime_detail,{index}')]]
    return InlineKeyboardMarkup(keyboard)
