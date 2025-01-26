"""Constants used throughout the application."""

# Conversation states
STATE_ANIME_NAME = "STATE_ANIME_NAME"
STATE_EDIT_DESCRIPTION = "STATE_EDIT_DESCRIPTION"
STATE_EDIT_EPISODE = "STATE_EDIT_EPISODE"

# Default values
DEFAULT_RATING = 0.0
DEFAULT_STATUS = "Not Started"
DEFAULT_EPISODES = 0
DEFAULT_DESCRIPTION = ""

# Status options
STATUS_WATCHING = "watching"
STATUS_COMPLETED = "completed"
STATUS_ON_HOLD = "on_hold"
STATUS_DROPPED = "dropped"
STATUS_PLANNED = "plan_to_watch"

# Button Status options
BUTTON_STATUS_WATCHING = "📺 Watching"
BUTTON_STATUS_COMPLETED = "✅ Completed"
BUTTON_STATUS_ON_HOLD = "⏸️ On Hold"
BUTTON_STATUS_DROPPED = "❌ Dropped"
BUTTON_STATUS_PLANNED = "📝 Plan to Watch"

# Message templates
WELCOME_MESSAGE = """
👋 Welcome! I'm your anime management bot.

Here are the available commands:
📺 Add Anime - Add an anime to your list
📚 My Anime List - View your anime collection

You can use these commands anytime by clicking the buttons below or typing:
/start or /s - Start the bot

/add_anime - Add an anime to your list

/get_animes - View your anime collection

/help or /h - Show this help message

Choose an option to get started!
"""

HELP_MESSAGE = """
📖 Help Guide

Available Commands:
/start or /s - Start the bot and see welcome message

/help or /h - Show this help message

/add_anime - Add a new anime to your list

/get_animes - View your anime collection

Features:
📺 Add Anime: Add new anime to your collection
📚 My Anime List: View and manage your anime
✏️ Edit Details: Change description, episodes, rating, and status
⭐ Rating System: Rate animes from 1 to 5 stars
📊 Status Tracking: Track your watching progress

Status Types:
📺 Watching - Currently watching
✅ Completed - Finished watching
⏸️ On Hold - Temporarily paused
❌ Dropped - Stopped watching
📝 Plan to Watch - Planning to watch

Need more help? Feel free to ask!
"""

UNAUTHORIZED_MESSAGE = """
⛔ Sorry, you are not authorized to use this bot.
Please contact the bot administrator for access.
"""
