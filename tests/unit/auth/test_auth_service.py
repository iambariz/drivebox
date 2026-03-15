"""Unit tests for GoogleDriveAuthService and CredentialRefreshService."""

from unittest.mock import MagicMock, patch

import pytest

from drivebox.auth.services import CredentialRefreshService, GoogleDriveAuthService


# --- CredentialRefreshService ---


@pytest.fixture
def credential_loader():
    return MagicMock()


@pytest.fixture
def refresh_service(credential_loader):
    return CredentialRefreshService(scopes=["scope1"], credential_loader=credential_loader)


def test_refresh_returns_creds_unchanged_when_valid(refresh_service):
    creds = MagicMock(expired=False)
    result = refresh_service.refresh_if_needed(creds)
    assert result == creds


def test_refresh_returns_none_when_creds_none(refresh_service):
    result = refresh_service.refresh_if_needed(None)
    assert result is None


def test_refresh_returns_none_when_no_refresh_token(refresh_service):
    creds = MagicMock(expired=True, refresh_token=None)
    result = refresh_service.refresh_if_needed(creds)
    assert result == creds


def test_refresh_calls_refresh_when_expired(refresh_service):
    creds = MagicMock(expired=True, refresh_token="token")
    with patch("drivebox.auth.services.Request"):
        result = refresh_service.refresh_if_needed(creds)
    creds.refresh.assert_called_once()
    assert result == creds


def test_refresh_returns_none_on_exception(refresh_service):
    creds = MagicMock(expired=True, refresh_token="token")
    creds.refresh.side_effect = Exception("network error")
    with patch("drivebox.auth.services.Request"):
        result = refresh_service.refresh_if_needed(creds)
    assert result is None


def test_create_new_credentials_raises_when_no_secrets(refresh_service, credential_loader):
    credential_loader.load.return_value = None
    with pytest.raises(FileNotFoundError, match="No client secrets"):
        refresh_service.create_new_credentials()


# --- GoogleDriveAuthService ---


@pytest.fixture
def token_storage():
    return MagicMock()


@pytest.fixture
def mock_refresh_service():
    return MagicMock()


@pytest.fixture
def auth_service(token_storage, mock_refresh_service):
    return GoogleDriveAuthService(
        token_storage=token_storage,
        refresh_service=mock_refresh_service,
    )


def test_get_credentials_returns_valid_cached_token(auth_service, token_storage):
    creds = MagicMock(valid=True)
    token_storage.load.return_value = creds
    result = auth_service.get_credentials()
    assert result == creds
    token_storage.save.assert_not_called()


def test_get_credentials_refreshes_when_expired(auth_service, token_storage, mock_refresh_service):
    expired = MagicMock(valid=False)
    refreshed = MagicMock(valid=True)
    token_storage.load.return_value = expired
    mock_refresh_service.refresh_if_needed.return_value = refreshed

    result = auth_service.get_credentials()

    assert result == refreshed
    token_storage.save.assert_called_once_with(refreshed)


def test_get_credentials_runs_oauth_when_refresh_fails(
    auth_service, token_storage, mock_refresh_service
):
    token_storage.load.return_value = None
    mock_refresh_service.refresh_if_needed.return_value = None
    new_creds = MagicMock(valid=True)
    mock_refresh_service.create_new_credentials.return_value = new_creds

    result = auth_service.get_credentials()

    assert result == new_creds
    mock_refresh_service.create_new_credentials.assert_called_once()
    token_storage.save.assert_called_once_with(new_creds)


def test_revoke_credentials_deletes_token(auth_service, token_storage):
    auth_service.revoke_credentials()
    token_storage.delete.assert_called_once()
