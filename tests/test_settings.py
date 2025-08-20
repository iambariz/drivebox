import json
import os
from pathlib import Path
import pytest

import drivebox.settings as settings


def test_load_settings_creates_default(tmp_path, monkeypatch):
    # Point SETTINGS_PATH to a temp dir
    fake_settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", fake_settings_path)

    # Ensure file doesn't exist
    assert not fake_settings_path.exists()

    result = settings.load_settings()

    # Should return defaults
    assert result == settings.DEFAULT_SETTINGS
    # File should now exist
    assert fake_settings_path.exists()

    # File contents should match defaults
    with open(fake_settings_path) as f:
        data = json.load(f)
    assert data == settings.DEFAULT_SETTINGS


def test_load_settings_reads_existing(tmp_path, monkeypatch):
    fake_settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", fake_settings_path)

    # Write custom settings
    custom = {"hotkey": "ctrl+shift+s", "user": "user123"}
    fake_settings_path.parent.mkdir(exist_ok=True)
    with open(fake_settings_path, "w") as f:
        json.dump(custom, f)

    result = settings.load_settings()

    # Should return the custom settings
    assert result == custom


def test_save_settings_writes_file(tmp_path, monkeypatch):
    fake_settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "SETTINGS_PATH", fake_settings_path)

    new_settings = {"hotkey": "ctrl+y", "sharing": "private"}
    settings.save_settings(new_settings)

    # File should exist
    assert fake_settings_path.exists()

    # File contents should match
    with open(fake_settings_path) as f:
        data = json.load(f)
    assert data == new_settings