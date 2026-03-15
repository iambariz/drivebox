"""Unit tests for PickleTokenStorage."""

from unittest.mock import MagicMock

import pytest

from drivebox.auth.token_storage import PickleTokenStorage


@pytest.fixture
def token_path(tmp_path):
    return tmp_path / ".drivebox" / "token.pickle"


@pytest.fixture
def file_service():
    mock = MagicMock()
    mock.ensure_directory.return_value = None
    return mock


@pytest.fixture
def storage(token_path, file_service):
    return PickleTokenStorage(token_path=token_path, file_service=file_service)


def test_ensures_directory_on_init(token_path, file_service):
    PickleTokenStorage(token_path=token_path, file_service=file_service)
    file_service.ensure_directory.assert_called_once_with(token_path.parent)


def test_load_returns_none_when_file_missing(storage, token_path):
    # token_path does not exist in tmp_path
    result = storage.load()
    assert result is None


def test_load_returns_credentials_when_file_exists(storage, token_path, file_service):
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.touch()
    fake_creds = MagicMock()
    file_service.read_pickle.return_value = fake_creds

    result = storage.load()
    assert result == fake_creds


def test_load_returns_none_on_corrupt_pickle(storage, token_path, file_service):
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.touch()
    file_service.read_pickle.side_effect = ValueError("bad pickle")

    result = storage.load()
    assert result is None


def test_save_calls_write_pickle(storage, token_path, file_service):
    fake_creds = MagicMock()
    storage.save(fake_creds)
    file_service.write_pickle.assert_called_once_with(token_path, fake_creds)


def test_delete_calls_delete_file(storage, token_path, file_service):
    file_service.delete_file.return_value = True
    storage.delete()
    file_service.delete_file.assert_called_once_with(token_path)
