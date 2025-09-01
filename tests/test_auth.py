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
        self._valid = valid
        self.expired = expired
        self.refresh_token = refresh_token
        self.refreshed = False

    @property
    def valid(self):
        # Simulate Google's behavior: valid if not expired and not forced invalid
        return self._valid and not self.expired

    def refresh(self, request):
        self.refreshed = True
        self._valid = True
        self.expired = False


# ---------------- get_gdrive_service ----------------

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


def test_get_gdrive_service_refresh_token(monkeypatch, tmp_path):
    fake_home = tmp_path
    token_file = fake_home / ".drivebox" / "token.pickle"
    token_file.parent.mkdir()

    creds = FakeCreds(valid=True, expired=True, refresh_token="refresh")
    token_file.write_bytes(pickle.dumps(creds))

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    with patch("drivebox.auth.build") as mock_build:
        service = auth.get_gdrive_service()
        assert mock_build.called

        # Reload the creds that were actually refreshed
        loaded = pickle.loads(token_file.read_bytes())
        assert loaded.refreshed is True


# ---------------- get_client_secrets ----------------

def test_get_client_secrets_from_keyring(monkeypatch):
    fake_json = {"installed": {"client_id": "abc"}}
    monkeypatch.setattr("drivebox.auth.keyring.get_password", lambda s, k: json.dumps(fake_json))

    result = auth.get_client_secrets()
    assert result == fake_json


def test_get_client_secrets_from_env(monkeypatch, tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text(json.dumps({"installed": {"client_id": "env"}}))

    monkeypatch.setenv("DRIVEBOX_CLIENT_SECRETS", str(creds_file))
    monkeypatch.setattr("drivebox.auth.keyring.get_password", lambda s, k: None)

    result = auth.get_client_secrets()
    assert result["installed"]["client_id"] == "env"


def test_get_client_secrets_from_fallback(monkeypatch, tmp_path):
    fake_home = tmp_path
    creds_file = fake_home / ".drivebox" / "credentials.json"
    creds_file.parent.mkdir()
    creds_file.write_text(json.dumps({"installed": {"client_id": "fallback"}}))

    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setattr("drivebox.auth.keyring.get_password", lambda s, k: None)
    monkeypatch.delenv("DRIVEBOX_CLIENT_SECRETS", raising=False)

    result = auth.get_client_secrets()
    assert result["installed"]["client_id"] == "fallback"


def test_get_client_secrets_not_found(monkeypatch, tmp_path):
    fake_home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setattr("drivebox.auth.keyring.get_password", lambda s, k: None)
    monkeypatch.delenv("DRIVEBOX_CLIENT_SECRETS", raising=False)

    with pytest.raises(FileNotFoundError):
        auth.get_client_secrets()


# ---------------- delete_token ----------------

def test_delete_token(monkeypatch, tmp_path):
    fake_home = tmp_path
    token_file = fake_home / ".drivebox" / "token.pickle"
    token_file.parent.mkdir()
    token_file.write_text("dummy")

    monkeypatch.setattr(Path, "home", lambda: fake_home)

    assert token_file.exists()
    auth.delete_token()
    assert not token_file.exists()