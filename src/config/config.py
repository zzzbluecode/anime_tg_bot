"""Configuration management for the application."""

import os
import logging
from typing import List
from dotenv import load_dotenv

logger = logging.getLogger()

class Config:
    """Configuration class for managing environment variables and settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        
        # Bot configuration
        self.bot_token = self._get_env('BOT_TOKEN')
        self.enable_restriction = self._get_env('ENABLE_USER_RESTRICTION', 'false').lower() == 'true'
        self.allowed_users = self._parse_allowed_users()
    
    def _get_env(self, key: str, default: str = None) -> str:
        """
        Get environment variable value.
        
        Args:
            key: Environment variable key
            default: Default value if key doesn't exist
            
        Returns:
            Value of environment variable or default
        """
        return os.getenv(key, default)
    
    def _parse_allowed_users(self) -> List[int]:
        """
        Parse allowed users from environment variable.
        
        Returns:
            List of allowed user IDs
        """
        allowed_users = []
        if self.enable_restriction:
            allowed_users_str = self._get_env('ALLOWED_USERS', '')
            if allowed_users_str:
                allowed_users = [
                    int(uid.strip()) 
                    for uid in allowed_users_str.split(',') 
                    if uid.strip().isdigit()
                ]
            logger.info(f"User restriction enabled. Allowed users: {allowed_users}")
        return allowed_users
