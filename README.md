# Anime Management Telegram Bot

A Telegram bot for managing your anime watchlist with features for tracking episodes, ratings, and status.

## Features

### Anime Management
- **Add Anime**: Add new anime to your watchlist using `/add_anime` command or "📺 Add Anime" button
- **View List**: Browse your anime collection using `/get_animes` command or "📚 My Anime List" button
- **Episode Tracking**: Keep track of watched episodes with increment/decrement controls
- **Detailed Information**: Each anime entry includes:
  - Description
  - Rating (1-5 stars)
  - Watch Status (Watching, Completed, On Hold, Dropped, Plan to Watch)
  - Episode Count

### Interactive Controls
- **Episode Management**:
  - ➕/➖ buttons to increment/decrement episodes
  - Direct episode number input
  - Current episode count display
- **Rating System**: Rate anime from ⭐ to ⭐⭐⭐⭐⭐
- **Status Updates**: Change watch status with predefined options
- **Easy Navigation**: Back buttons and intuitive menu structure

## Commands
- `/start` - Start the bot and see available commands
- `/add_anime` - Add a new anime to your list
- `/get_animes` - View your anime collection
- `/help` - Show help message with available commands

## Setup Instructions

1. **Prerequisites**:
   - Python 3.7 or higher
   - pip (Python package installer)

2. **Installation**:
   ```bash
   # Clone the repository
   git clone [repository-url]
   cd [repository-name]

   # Install required packages
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Create a `.env` file in the project root
   - Add your Telegram bot token:
     ```
     BOT_TOKEN=your_bot_token_here

     # Optional: Enable user restriction
     ENABLE_USER_RESTRICTION=true
     
     # Add allowed user IDs (comma-separated)
     ALLOWED_USERS=123456789,987654321
     ```
   - User restriction is disabled by default. Set `ENABLE_USER_RESTRICTION=true` to enable it
   - When enabled, only users with IDs listed in `ALLOWED_USERS` can use the bot
   - To get a user's Telegram ID, you can:
     1. Start a chat with @userinfobot on Telegram
     2. Forward a message from the user to @userinfobot
     3. Use other Telegram bots that provide user ID information

4. **Running the Bot**:
   ```bash
   python main.py
   ```

## Usage

1. **Adding an Anime**:
   - Click "📺 Add Anime" or use `/add_anime`
   - Enter the anime name
   - The anime will be added to your list with default values

2. **Viewing Your List**:
   - Click "📚 My Anime List" or use `/get_animes`
   - Click on any anime to view its details

3. **Managing Episodes**:
   - In anime details, click "🎬 Edit Episodes"
   - Use ➕/➖ to adjust episode count
   - Click the number to enter a specific episode number

4. **Editing Details**:
   - Click on an anime in your list
   - Use the edit buttons to modify:
     - Description
     - Rating
     - Status
     - Episodes

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License.
