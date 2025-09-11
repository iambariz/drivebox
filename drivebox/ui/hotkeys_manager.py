from drivebox.settings import load_settings, save_settings

class HotkeysManager:
    DEFAULTS = {
        "fullscreen": ("Fullscreen Screenshot", "Ctrl+Alt+X"),
        "region": ("Region Screenshot", "Ctrl+Alt+R"),
        "record_start": ("Start Recording", "Ctrl+Alt+S"),
        "record_stop": ("Stop Recording", "Ctrl+Alt+E"),
    }

    def __init__(self):
        self._settings = load_settings()
        self._hotkeys = self._settings.get("hotkeys", {}).copy()

    def get(self, action: str) -> str:
        """Return the current hotkey for an action, or default if none set."""
        return self._hotkeys.get(action, self.DEFAULTS[action][1])

    def set(self, action: str, hotkey: str):
        """Update hotkey for an action."""
        if any(v == hotkey for k, v in self._hotkeys.items() if k != action):
            raise ValueError(f"Hotkey {hotkey} is already assigned to another action.")
        self._hotkeys[action] = hotkey
        self._persist()

    def reset(self, action: str):
        """Reset to default hotkey for an action."""
        self._hotkeys[action] = self.DEFAULTS[action][1]
        self._persist()

    def all(self) -> dict:
        """Return a dict {action: hotkey} with current values."""
        return {action: self.get(action) for action in self.DEFAULTS}

    def _persist(self):
        self._settings["hotkeys"] = self._hotkeys
        save_settings(self._settings)