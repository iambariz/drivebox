import json
from pathlib import Path

SETTINGS_PATH = Path.home() / ".drivebox" / "settings.json"

DEFAULT_SETTINGS = {
    "hotkey": "ctrl+alt+x",
    "hotkey_region": "ctrl+alt+r",
    "sharing": "anyone",
    "user": None
}

def load_settings():
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    else:
        SETTINGS_PATH.parent.mkdir(exist_ok=True)
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    SETTINGS_PATH.parent.mkdir(exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
