import os
import sys
import pickle
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import keyring

SCOPES = ['https://www.googleapis.com/auth/drive.file']

SERVICE_NAME = "drivebox"
CREDENTIALS_KEY = "google_client_secrets"


def get_token_path():
    # Use a hidden folder in the user's home directory
    app_dir = Path.home() / ".drivebox"
    app_dir.mkdir(exist_ok=True)
    return app_dir / "token.pickle"


def get_client_secrets():
    """Retrieve Google client secrets from keyring or fallback file/env."""
    # 1. Try keyring
    creds_json = keyring.get_password(SERVICE_NAME, CREDENTIALS_KEY)
    if creds_json:
        return json.loads(creds_json)

    # 2. Try environment variable
    env_path = os.environ.get("DRIVEBOX_CLIENT_SECRETS")
    if env_path and os.path.exists(env_path):
        with open(env_path, "r") as f:
            return json.load(f)

    # 3. Try user config file (~/.drivebox/credentials.json)
    fallback_path = Path.home() / ".drivebox" / "credentials.json"
    if fallback_path.exists():
        with open(fallback_path, "r") as f:
            return json.load(f)

    raise FileNotFoundError(
        "No Google client secrets found. "
        "Run `scripts/store_credentials.py` or place credentials.json in ~/.drivebox/"
    )


def get_gdrive_service():
    creds = None
    token_path = get_token_path()

    # Load existing token if available
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secrets = get_client_secrets()
            flow = InstalledAppFlow.from_client_config(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def delete_token():
    token_path = get_token_path()
    if token_path.exists():
        token_path.unlink()