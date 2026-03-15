"""Unit tests for DriveClient."""

from unittest.mock import MagicMock

import pytest

from drivebox.drive.client import DriveClient


@pytest.fixture
def service():
    return MagicMock()


@pytest.fixture
def client(service):
    return DriveClient(service)


def test_upload_file_returns_file_id(client, service):
    service.files().create().execute.return_value = {"id": "abc123"}
    file_id = client.upload_file(b"data", "shot.png")
    assert file_id == "abc123"


def test_upload_file_raises_if_no_id(client, service):
    service.files().create().execute.return_value = {}
    with pytest.raises(ValueError, match="no file ID"):
        client.upload_file(b"data", "shot.png")


def test_upload_file_sets_folder_parent(client, service):
    service.files().create().execute.return_value = {"id": "abc123"}
    client.upload_file(b"data", "shot.png", folder_id="folder456")
    call_kwargs = service.files().create.call_args[1]
    assert call_kwargs["body"]["parents"] == ["folder456"]


def test_upload_file_no_parent_when_no_folder(client, service):
    service.files().create().execute.return_value = {"id": "abc123"}
    client.upload_file(b"data", "shot.png")
    call_kwargs = service.files().create.call_args[1]
    assert "parents" not in call_kwargs["body"]


def test_get_shareable_link_returns_url(client, service):
    service.permissions().create().execute.return_value = {}
    link = client.get_shareable_link("abc123")
    assert link == "https://drive.google.com/file/d/abc123/view"


def test_get_shareable_link_sets_public_permission(client, service):
    service.permissions().create().execute.return_value = {}
    client.get_shareable_link("abc123")
    call_kwargs = service.permissions().create.call_args[1]
    assert call_kwargs["body"] == {"type": "anyone", "role": "reader"}


def test_upload_and_share_returns_link(client, service):
    service.files().create().execute.return_value = {"id": "abc123"}
    service.permissions().create().execute.return_value = {}
    link = client.upload_and_share(b"data", "shot.png")
    assert link == "https://drive.google.com/file/d/abc123/view"
