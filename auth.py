import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Build the Drive service
    service = build('drive', 'v3', credentials=creds)
    return service

if __name__ == "__main__":
    service = get_gdrive_service()

    # Search for 'drivebox' folder at the root
    query = (
        "name = 'drivebox' and "
        "mimeType = 'application/vnd.google-apps.folder' and "
        "'root' in parents"
    )
    response = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=10
    ).execute()

    folders = response.get('files', [])
    if not folders:
        print("No 'drivebox' folder found at root. Creating one...")
        file_metadata = {
            'name': 'drivebox',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['root']
        }
        folder = service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        print(f"Created folder: {folder['name']} (ID: {folder['id']})")
    else:
        print("'drivebox' folder(s) at root:")
        for folder in folders:
            print(f"Name: {folder['name']}, ID: {folder['id']}")
