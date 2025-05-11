import os
import sys
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_token_path():
    # Use a hidden folder in the user's home directory
    app_dir = Path.home() / ".drivebox"
    app_dir.mkdir(exist_ok=True)
    return app_dir / "token.pickle"

def get_gdrive_service():
    creds = None
    token_path = get_token_path()
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                resource_path('credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def delete_token():
    token_path = get_token_path()
    if token_path.exists():
        token_path.unlink()

def resource_path(filename):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)