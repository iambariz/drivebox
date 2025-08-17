import os
from googleapiclient.http import MediaFileUpload
from drivebox.auth import get_gdrive_service
from drivebox.settings import load_settings

def get_drivebox_folder_id(service):
    query = (
        "name = 'drivebox' and "
        "mimeType = 'application/vnd.google-apps.folder' and "
        "'root' in parents"
    )
    response = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()
    folders = response.get('files', [])
    if folders:
        return folders[0]['id']
    file_metadata = {
        'name': 'drivebox',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['root']
    }
    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()
    return folder['id']

def upload_file_to_drivebox(filepath):
    service = get_gdrive_service()
    folder_id = get_drivebox_folder_id(service)
    file_metadata = {
        'name': os.path.basename(filepath),
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    # Set sharing based on settings
    settings = load_settings()
    if settings.get("sharing", "anyone") == "anyone":
        service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
    print(f"Uploaded! Shareable link: {file['webViewLink']}")
    return file['webViewLink']
