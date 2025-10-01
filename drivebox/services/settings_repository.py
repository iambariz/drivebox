from typing import Optional, Dict
from drivebox.settings import load_settings, save_settings


class SettingsRepository:
    """Manages application settings with caching."""
    
    def __init__(self):
        self._settings = None
    
    def _load(self) -> Dict:
        """Lazy load settings."""
        if self._settings is None:
            self._settings = load_settings()
        return self._settings
    
    def _save(self) -> None:
        """Persist settings to disk."""
        if self._settings is not None:
            save_settings(self._settings)
    
    def get_user(self) -> Optional[Dict[str, str]]:
        """Get current user information."""
        return self._load().get("user")
    
    def set_user(self, user: Optional[Dict[str, str]]) -> None:
        """Set user information and save."""
        self._load()["user"] = user
        self._save()
    
    def get_sharing_mode(self) -> str:
        """Get sharing mode: 'anyone' or 'private'."""
        return self._load().get("sharing", "anyone")
    
    def set_sharing_mode(self, mode: str) -> None:
        """Set sharing mode and save."""
        self._load()["sharing"] = mode
        self._save()