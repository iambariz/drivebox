"""Google Drive authentication services."""

import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

from drivebox.auth.credential_loaders import (
    ChainedCredentialLoader,
    EnvironmentCredentialLoader,
    FileCredentialLoader,
    KeyringCredentialLoader,
)
from drivebox.auth.token_storage import PickleTokenStorage
from drivebox.config import (
    CREDENTIALS_KEY,
    ENV_VAR_CREDENTIALS,
    GOOGLE_DRIVE_SCOPES,
    SERVICE_NAME,
    AppSettings,
)
from drivebox.storage import SecureFileService


logger = logging.getLogger(__name__)


class CredentialRefreshService:
    def __init__(self, scopes: list[str], credential_loader: ChainedCredentialLoader):
        self.scopes = scopes
        self.credential_loader = credential_loader

    def refresh_if_needed(self, creds: Credentials | None) -> Credentials | None:
        if not creds or not creds.expired or not creds.refresh_token:
            return creds

        try:
            creds.refresh(Request())
        except Exception:
            logger.exception("Refresh failed")
            return None
        else:
            logger.info("Credentials refreshed")
            return creds

    def create_new_credentials(self) -> Credentials:
        """Opens browser for OAuth - THIS IS THE POPUP!"""
        client_secrets = self.credential_loader.load()
        if not client_secrets:
            raise FileNotFoundError(
                "No client secrets available. "
                "Configure credentials via keyring, DRIVEBOX_CLIENT_SECRETS env, "
                "or ~/.drivebox/credentials.json"
            )

        flow = InstalledAppFlow.from_client_config(client_secrets, self.scopes)
        creds = flow.run_local_server(port=0)
        logger.info("New credentials obtained via OAuth")
        return creds


class GoogleDriveAuthService:
    def __init__(
        self,
        token_storage: PickleTokenStorage,
        refresh_service: CredentialRefreshService,
    ):
        self.token_storage = token_storage
        self.refresh_service = refresh_service

    def get_credentials(self) -> Credentials:
        creds = self.token_storage.load()

        if creds and creds.valid:
            return creds

        creds = self.refresh_service.refresh_if_needed(creds)

        if not creds or not creds.valid:
            creds = self.refresh_service.create_new_credentials()

        self.token_storage.save(creds)
        return creds

    def get_service(self) -> Resource:
        creds = self.get_credentials()
        return build("drive", "v3", credentials=creds)

    def revoke_credentials(self) -> None:
        self.token_storage.delete()


class GoogleDriveAuthServiceFactory:
    @classmethod
    def create(cls, settings: AppSettings | None = None) -> GoogleDriveAuthService:
        if settings is None:
            settings = AppSettings()

        file_service = SecureFileService()

        credential_loader = ChainedCredentialLoader(
            [
                KeyringCredentialLoader(SERVICE_NAME, CREDENTIALS_KEY),
                EnvironmentCredentialLoader(ENV_VAR_CREDENTIALS, file_service),
                FileCredentialLoader(settings.credentials_path, file_service),
            ]
        )

        token_storage = PickleTokenStorage(settings.token_path, file_service)
        refresh_service = CredentialRefreshService(GOOGLE_DRIVE_SCOPES, credential_loader)

        return GoogleDriveAuthService(
            token_storage=token_storage,
            refresh_service=refresh_service,
        )


def get_gdrive_service() -> Resource:
    return GoogleDriveAuthServiceFactory.create().get_service()


def delete_token() -> None:
    GoogleDriveAuthServiceFactory.create().revoke_credentials()
