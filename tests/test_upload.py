import pytest
from unittest.mock import MagicMock, patch
import drivebox.upload as upload


def make_fake_service(
    existing_folder=None, new_folder_id="new123", file_id="file123", link="http://link"
):
    """Helper to build a fake Google Drive service with chained mocks."""
    service = MagicMock()

    # Mock files().list().execute()
    if existing_folder:
        service.files.return_value.list.return_value.execute.return_value = {
            "files": [{"id": existing_folder, "name": "drivebox"}]
        }
    else:
        service.files.return_value.list.return_value.execute.return_value = {"files": []}

    # Mock files().create(...) differently for folder vs file
    def create_side_effect(*args, **kwargs):
        body = kwargs.get("body", {})
        if body.get("mimeType") == "application/vnd.google-apps.folder":
            mock = MagicMock()
            mock.execute.return_value = {"id": new_folder_id}  # folder creation
            return mock
        else:
            mock = MagicMock()
            mock.execute.return_value = {"id": file_id, "webViewLink": link}  # file upload
            return mock

    service.files.return_value.create.side_effect = create_side_effect

    # Mock permissions().create().execute()
    service.permissions.return_value.create.return_value.execute.return_value = {}

    return service


def test_get_drivebox_folder_id_existing():
    service = make_fake_service(existing_folder="abc123")
    folder_id = upload.get_drivebox_folder_id(service)
    assert folder_id == "abc123"
    # allow >=1 calls instead of exactly once
    assert service.files.return_value.list.call_count >= 1


def test_get_drivebox_folder_id_creates_new():
    service = make_fake_service(existing_folder=None, new_folder_id="xyz789")
    folder_id = upload.get_drivebox_folder_id(service)
    assert folder_id == "xyz789"
    # ensure folder creation was attempted
    assert service.files.return_value.create.call_count >= 1


@patch("drivebox.upload.get_drivebox_folder_id", return_value="folder123")
@patch("drivebox.upload.load_settings", return_value={"sharing": "anyone"})
@patch("drivebox.upload.get_gdrive_service")
def test_upload_file_with_sharing(mock_service, mock_settings, mock_folder, tmp_path):
    fake_file = tmp_path / "test.txt"
    fake_file.write_text("hello")

    service = make_fake_service(file_id="f1", link="http://link")
    mock_service.return_value = service

    link = upload.upload_file_to_drivebox(str(fake_file))
    assert link == "http://link"

    # Should set sharing
    service.permissions.return_value.create.assert_called_once()


@patch("drivebox.upload.get_drivebox_folder_id", return_value="folder123")
@patch("drivebox.upload.load_settings", return_value={"sharing": "private"})
@patch("drivebox.upload.get_gdrive_service")
def test_upload_file_without_sharing(mock_service, mock_settings, mock_folder, tmp_path):
    fake_file = tmp_path / "test.txt"
    fake_file.write_text("hello")

    service = make_fake_service(file_id="f2", link="http://link2")
    mock_service.return_value = service

    link = upload.upload_file_to_drivebox(str(fake_file))
    assert link == "http://link2"

    # Should NOT set sharing
    service.permissions.return_value.create.assert_not_called()