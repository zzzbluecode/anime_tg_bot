"""Models for anime data management."""

from dataclasses import dataclass
from typing import Dict, Optional, List
import json

from src.constant.constant import (
    DEFAULT_DESCRIPTION,
    DEFAULT_RATING,
    DEFAULT_STATUS,
    DEFAULT_EPISODES
)

@dataclass
class AnimeDetails:
    """Class to store details of an anime."""
    
    name: str
    description: str = DEFAULT_DESCRIPTION
    rating: float = DEFAULT_RATING
    status: str = DEFAULT_STATUS
    episodes: int = DEFAULT_EPISODES

    def to_dict(self) -> Dict:
        """
        Convert the anime details to a dictionary format.
        
        Returns:
            Dictionary representation of anime details
        """
        return {
            'description': self.description,
            'rating': self.rating,
            'status': self.status,
            'episodes': self.episodes
        }

    @classmethod
    def from_dict(cls, name: str, details: Dict) -> 'AnimeDetails':
        """
        Create an AnimeDetails instance from a dictionary.
        
        Args:
            name: Name of the anime
            details: Dictionary containing anime details
            
        Returns:
            New AnimeDetails instance
        """
        return cls(
            name=name,
            description=details.get('description', DEFAULT_DESCRIPTION),
            rating=float(details.get('rating', DEFAULT_RATING)),
            status=details.get('status', DEFAULT_STATUS),
            episodes=int(details.get('episodes', DEFAULT_EPISODES))
        )


class AnimeDetailsManager:
    """Class to manage a collection of anime details."""
    
    def __init__(self):
        """Initialize the AnimeDetailsManager with a specified config."""
        self.config = 'anime_config.json'
        self.anime_list: List[str] = []
        self.anime_details: Dict[str, AnimeDetails] = {}
        try:
            self.load_anime_list_from_config()
        except Exception as e:
            pass

    def load_anime_list_from_config(self) -> None:
        """Load the default anime list from the specified JSON file."""
        with open(self.config, 'r') as file:
            data = json.load(file)
            for name, details in data.items():
                self.anime_list.append(name)
                self.anime_details[name] = AnimeDetails.from_dict(name, details)

    def add_anime(self, name: str) -> None:
        """
        Add a new anime to the collection and update the file.
        """
        if name not in self.anime_list:
            self.anime_list.append(name)
            self.anime_details[name] = AnimeDetails(name=name)
            self.update_anime_config()

    def update_anime_config(self) -> None:
        """Update the anime list in the specified JSON file with full anime details."""
        with open(self.config, 'w') as file:
            json_data = {anime.name: anime.to_dict() for anime in self.anime_details.values()}
            json.dump(json_data, file, indent=4)

    def get_anime(self, name: str) -> Optional[AnimeDetails]:
        """
        Get anime details by name.
        
        Args:
            name: Name of the anime to retrieve
            
        Returns:
            AnimeDetails if found, None otherwise
        """
        return self.anime_details.get(name)

    def update_anime(self, name: str, **kwargs) -> bool:
        """
        Update anime details and write the updated list to the file.
        """
        if name not in self.anime_details:
            return False
        for key, value in kwargs.items():
            if key in self.anime_details[name].__dict__:
                setattr(self.anime_details[name], key, value)
        self.update_anime_config()
        return True

    def get_all_animes(self) -> List[AnimeDetails]:
        """
        Get list of all anime details.
        
        Returns:
            List of all AnimeDetails instances
        """
        return [self.anime_details[name] for name in self.anime_list]

    def get_anime_by_index(self, index: int) -> Optional[AnimeDetails]:
        """
        Get anime details by index.
        
        Args:
            index: Index in the anime list
            
        Returns:
            AnimeDetails if found, None otherwise
        """
        if 0 <= index < len(self.anime_list):
            name = self.anime_list[index]
            return self.anime_details[name]
        return None

    def to_dict(self) -> Dict:
        """
        Convert all anime details to dictionary format.
        
        Returns:
            Dictionary containing all anime details
        """
        return {name: details.to_dict() for name, details in self.anime_details.items()}

    @classmethod
    def from_dict(cls, data: Dict) -> 'AnimeDetailsManager':
        """
        Create an AnimeDetailsManager instance from a dictionary.
        
        Args:
            data: Dictionary containing anime data
            
        Returns:
            New AnimeDetailsManager instance
        """
        manager = cls()
        for name in data:
            manager.anime_list.append(name)
            manager.anime_details[name] = AnimeDetails.from_dict(name, data[name])
        return manager
