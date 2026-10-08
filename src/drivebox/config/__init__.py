"""Configuration module."""

from .constants import (
    CREDENTIALS_KEY,
    ENV_VAR_CREDENTIALS,
    GOOGLE_DRIVE_SCOPES,
    OAUTH_TIMEOUT_SECONDS,
    SERVICE_NAME,
)
from .settings import AppSettings


__all__ = [
    "AppSettings",
    "GOOGLE_DRIVE_SCOPES",
    "SERVICE_NAME",
    "CREDENTIALS_KEY",
    "ENV_VAR_CREDENTIALS",
    "OAUTH_TIMEOUT_SECONDS",
]
