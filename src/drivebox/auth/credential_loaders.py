"""Credential loading strategies."""

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import keyring

from drivebox.storage import SecureFileService


logger = logging.getLogger(__name__)


class BaseCredentialLoader(ABC):
    @abstractmethod
    def load(self) -> dict[str, Any] | None:
        pass


class KeyringCredentialLoader(BaseCredentialLoader):
    def __init__(self, service_name: str, key: str):
        self.service_name = service_name
        self.key = key

    def load(self) -> dict[str, Any] | None:
        creds_json = keyring.get_password(self.service_name, self.key)
        if not creds_json:
            return None

        try:
            data: dict[str, Any] = json.loads(creds_json)
        except json.JSONDecodeError:
            logger.exception("Invalid JSON in keyring")
            return None
        else:
            return data


class EnvironmentCredentialLoader(BaseCredentialLoader):
    def __init__(self, env_var: str, file_service: SecureFileService):
        self.env_var = env_var
        self.file_service = file_service

    def load(self) -> dict[str, Any] | None:
        env_path = os.environ.get(self.env_var)
        if not env_path:
            return None

        path = Path(env_path)
        if not path.exists():
            return None

        try:
            return self.file_service.read_json(path)
        except ValueError:
            logger.exception("Environment credential load failed")
            return None


class FileCredentialLoader(BaseCredentialLoader):
    def __init__(self, path: Path, file_service: SecureFileService):
        self.path = path
        self.file_service = file_service

    def load(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None

        try:
            return self.file_service.read_json(self.path)
        except ValueError:
            logger.exception("File credential load failed")
            return None


class ChainedCredentialLoader(BaseCredentialLoader):
    def __init__(self, loaders: list[BaseCredentialLoader]):
        self.loaders = loaders

    def load(self) -> dict[str, Any] | None:
        for loader in self.loaders:
            result = loader.load()
            if result:
                logger.info(f"Credentials loaded via {loader.__class__.__name__}")
                return result
        return None
