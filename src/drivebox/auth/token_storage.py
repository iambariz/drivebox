"""Token storage implementations."""

import logging
from pathlib import Path

from google.oauth2.credentials import Credentials

from drivebox.storage import SecureFileService


logger = logging.getLogger(__name__)


class PickleTokenStorage:
    def __init__(self, token_path: Path, file_service: SecureFileService):
        self.token_path = token_path
        self.file_service = file_service
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        self.file_service.ensure_directory(self.token_path.parent)

    def load(self) -> Credentials | None:
        if not self.token_path.exists():
            return None

        try:
            creds = self.file_service.read_pickle(self.token_path)
        except ValueError as e:
            logger.warning(f"Token load failed: {e}")
            return None
        else:
            logger.info("Token loaded from storage")
            return creds

    def save(self, creds: Credentials) -> None:
        self.file_service.write_pickle(self.token_path, creds)
        logger.info("Token saved to storage")

    def delete(self) -> None:
        if self.file_service.delete_file(self.token_path):
            logger.info("Token deleted from storage")
