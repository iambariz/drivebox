"""Unit tests for AppSettings."""

from pathlib import Path
from unittest.mock import patch

from drivebox.config.settings import AppSettings


def test_default_token_path():
    with patch.object(Path, "mkdir"):
        settings = AppSettings(app_dir=Path("/tmp/.drivebox"))
    assert settings.token_path == Path("/tmp/.drivebox/token.pickle")


def test_default_credentials_path():
    with patch.object(Path, "mkdir"):
        settings = AppSettings(app_dir=Path("/tmp/.drivebox"))
    assert settings.credentials_path == Path("/tmp/.drivebox/credentials.json")


def test_custom_token_filename():
    with patch.object(Path, "mkdir"):
        settings = AppSettings(app_dir=Path("/tmp/.drivebox"), token_filename="custom.pkl")
    assert settings.token_path.name == "custom.pkl"
