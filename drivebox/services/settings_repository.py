from __future__ import annotations
from typing import Optional, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal
from drivebox.settings import load_settings, save_settings


class SettingsRepository(QObject):
    """
    Manages application settings with lazy caching and Qt signals for live updates.
    Persists via drivebox.settings.load_settings/save_settings.
    """

    # Signals
    auth_changed = pyqtSignal(object)        # emits user dict or None
    sharing_mode_changed = pyqtSignal(str)   # emits "anyone" | "private"

    def __init__(self):
        super().__init__()
        self._settings: Dict[str, Any] | None = None

    # Internal cache helpers
    def _load(self) -> Dict[str, Any]:
        if self._settings is None:
            self._settings = load_settings()
            # Ensure defaults if missing
            if "sharing" not in self._settings:
                self._settings["sharing"] = "private"
            # Optional: normalize user to None if invalid
            if not self._settings.get("user"):
                self._settings["user"] = None
        return self._settings
    
    def _save(self) -> None:
        if self._settings is not None:
            save_settings(self._settings)

    # Public API: Auth
    def get_user(self) -> Optional[Dict[str, str]]:
        """Get current user information."""
        return self._load().get("user")
    
    def set_user(self, user: Optional[Dict[str, str]]) -> None:
        current = self.get_user()
        if current == user:
            return
        self._load()["user"] = self._sanitize_user(user)
        self._save()
        self.auth_changed.emit(self._load()["user"])

    # Public API: Sharing
    def get_sharing_mode(self) -> str:
        mode = self._load().get("sharing", "private")
        return mode if mode in ("anyone", "private") else "private"

    def set_sharing_mode(self, mode: str) -> None:
        mode = mode or "private"
        if mode not in ("anyone", "private"):
            return
        current = self.get_sharing_mode()
        if current == mode:
            return
        self._load()["sharing"] = mode
        self._save()
        self.sharing_mode_changed.emit(mode)

    # Utilities
    def clear_all(self) -> None:
        """
        Optional helper for tests or a 'Reset settings' action.
        Clears cache and persists defaults, emitting signals.
        """
        self._settings = {"user": None, "sharing": "private"}
        self._save()
        self.auth_changed.emit(None)
        self.sharing_mode_changed.emit("private")

    def _sanitize_user(self, user: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        if not user:
            return None
        # Keep only safe, minimal fields used by UI
        return {
            "name": user.get("name") or "",
            "email": user.get("email") or "",
        }