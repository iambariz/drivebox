"""Google Drive upload client."""

import io
import logging
from typing import Any

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaIoBaseUpload


logger = logging.getLogger(__name__)


class DriveClient:
    def __init__(self, service: Resource):
        self.service = service

    def upload_file(
        self,
        file_data: bytes,
        filename: str,
        mime_type: str = "image/png",
        folder_id: str | None = None,
    ) -> str:
        """Upload file to Google Drive and return file ID."""
        file_metadata: dict[str, Any] = {"name": filename}

        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaIoBaseUpload(
            io.BytesIO(file_data),
            mimetype=mime_type,
            resumable=True,
        )

        file = (
            self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        )

        file_id: str | None = file.get("id")
        if not file_id:
            raise ValueError("Upload failed: no file ID returned")

        logger.info(f"Uploaded file: {filename} (ID: {file_id})")
        return file_id

    def get_shareable_link(self, file_id: str) -> str:
        """Make file publicly accessible and return shareable link."""
        permission = {"type": "anyone", "role": "reader"}

        self.service.permissions().create(
            fileId=file_id,
            body=permission,
        ).execute()

        logger.info(f"Made file {file_id} publicly shareable")

        return f"https://drive.google.com/file/d/{file_id}/view"

    def upload_and_share(
        self,
        file_data: bytes,
        filename: str,
        mime_type: str = "image/png",
        folder_id: str | None = None,
    ) -> str:
        """Upload file and return shareable link."""
        file_id = self.upload_file(file_data, filename, mime_type, folder_id)
        return self.get_shareable_link(file_id)
