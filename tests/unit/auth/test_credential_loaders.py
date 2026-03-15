"""Unit tests for credential loaders."""

import json
from unittest.mock import MagicMock, patch

from drivebox.auth.credential_loaders import (
    ChainedCredentialLoader,
    EnvironmentCredentialLoader,
    FileCredentialLoader,
    KeyringCredentialLoader,
)


# --- KeyringCredentialLoader ---


@patch(
    "drivebox.auth.credential_loaders.keyring.get_password",
    return_value=json.dumps({"client_id": "x"}),
)
def test_keyring_loader_returns_dict(mock_keyring):
    loader = KeyringCredentialLoader(service_name="drivebox", key="credentials")
    result = loader.load()
    assert result == {"client_id": "x"}


@patch("drivebox.auth.credential_loaders.keyring.get_password", return_value=None)
def test_keyring_loader_returns_none_when_empty(mock_keyring):
    loader = KeyringCredentialLoader(service_name="drivebox", key="credentials")
    assert loader.load() is None


@patch("drivebox.auth.credential_loaders.keyring.get_password", return_value="not-json")
def test_keyring_loader_returns_none_on_invalid_json(mock_keyring):
    loader = KeyringCredentialLoader(service_name="drivebox", key="credentials")
    assert loader.load() is None


# --- FileCredentialLoader ---


def test_file_loader_returns_dict_when_file_exists(tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.touch()
    file_service = MagicMock()
    file_service.read_json.return_value = {"client_id": "y"}
    loader = FileCredentialLoader(path=creds_file, file_service=file_service)
    assert loader.load() == {"client_id": "y"}


def test_file_loader_returns_none_when_file_missing(tmp_path):
    missing = tmp_path / "missing.json"
    loader = FileCredentialLoader(path=missing, file_service=MagicMock())
    assert loader.load() is None


def test_file_loader_returns_none_on_read_error(tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.touch()
    file_service = MagicMock()
    file_service.read_json.side_effect = ValueError("bad")
    loader = FileCredentialLoader(path=creds_file, file_service=file_service)
    assert loader.load() is None


# --- EnvironmentCredentialLoader ---


def test_env_loader_returns_none_when_var_not_set():
    file_service = MagicMock()
    loader = EnvironmentCredentialLoader(
        env_var="DRIVEBOX_CLIENT_SECRETS", file_service=file_service
    )
    with patch.dict("os.environ", {}, clear=True):
        assert loader.load() is None


def test_env_loader_returns_none_when_file_missing(tmp_path):
    file_service = MagicMock()
    loader = EnvironmentCredentialLoader(
        env_var="DRIVEBOX_CLIENT_SECRETS", file_service=file_service
    )
    with patch.dict("os.environ", {"DRIVEBOX_CLIENT_SECRETS": str(tmp_path / "missing.json")}):
        assert loader.load() is None


def test_env_loader_returns_dict_when_file_exists(tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text(json.dumps({"client_id": "z"}))
    file_service = MagicMock()
    file_service.read_json.return_value = {"client_id": "z"}
    loader = EnvironmentCredentialLoader(
        env_var="DRIVEBOX_CLIENT_SECRETS", file_service=file_service
    )
    with patch.dict("os.environ", {"DRIVEBOX_CLIENT_SECRETS": str(creds_file)}):
        result = loader.load()
    assert result == {"client_id": "z"}


# --- ChainedCredentialLoader ---


def test_chained_loader_returns_first_success():
    failing = MagicMock()
    failing.load.return_value = None
    succeeding = MagicMock()
    succeeding.load.return_value = {"client_id": "found"}
    skipped = MagicMock()

    loader = ChainedCredentialLoader([failing, succeeding, skipped])
    result = loader.load()

    assert result == {"client_id": "found"}
    skipped.load.assert_not_called()


def test_chained_loader_returns_none_when_all_fail():
    loaders = [MagicMock(load=MagicMock(return_value=None)) for _ in range(3)]
    loader = ChainedCredentialLoader(loaders)
    assert loader.load() is None
