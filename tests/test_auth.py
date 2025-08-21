import os
import json
import pickle
from pathlib import Path
from unittest.mock import patch
import pytest

import drivebox.auth as auth


class FakeCreds:
    """Minimal fake credentials object that can be pickled."""
    def __init__(self, valid=True, expired=False, refresh_token=None):
        self.valid = valid
        self.expired = expired
        self.refresh_token = refresh_token
        self.refreshed = False

    def refresh(self, request):
        self.refreshed = True


def test_get_gdrive_service_with_existing_token(tmp_path, monkeypatch):
    fake_home = tmp_path
    token_file = fake_home / ".drivebox" / "token.pickle"
    token_file.parent.mkdir()

    creds = FakeCreds(valid=True)
    token_file.write_bytes(pickle.dumps(creds))

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    with patch("drivebox.auth.build") as mock_build:
        service = auth.get_gdrive_service()
        assert mock_build.called
        assert service == mock_build.return_value


def test_get_gdrive_service_new_token(monkeypatch, tmp_path):
    fake_home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    # No token file
    monkeypatch.setattr("drivebox.auth.get_client_secrets", lambda: {"installed": {"client_id": "abc"}})

    fake_creds = FakeCreds(valid=True)
    fake_flow = type("FakeFlow", (), {"run_local_server": lambda self, port=0: fake_creds})()

    with patch("drivebox.auth.InstalledAppFlow.from_client_config", return_value=fake_flow), \
         patch("drivebox.auth.build") as mock_build:
        service = auth.get_gdrive_service()
        assert mock_build.called
        assert service == mock_build.return_value

        # Ensure token file was written with picklable creds
        token_file = fake_home / ".drivebox" / "token.pickle"
        assert token_file.exists()
        loaded = pickle.loads(token_file.read_bytes())
        assert isinstance(loaded, FakeCreds)