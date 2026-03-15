"""Unit tests for ScreenshotService."""

from unittest.mock import MagicMock

import pytest

from drivebox.services.screenshot_service import ScreenshotService


@pytest.fixture
def capture():
    mock = MagicMock()
    mock.capture_fullscreen.return_value = b"png_bytes"
    mock.generate_filename.return_value = "screenshot_20260315_120000.png"
    return mock


@pytest.fixture
def drive_client():
    mock = MagicMock()
    mock.upload_and_share.return_value = "https://drive.google.com/file/d/abc123/view"
    return mock


@pytest.fixture
def clipboard():
    return MagicMock()


@pytest.fixture
def service(capture, drive_client, clipboard):
    return ScreenshotService(capture=capture, drive_client=drive_client, clipboard=clipboard)


def test_returns_shareable_link(service, drive_client):
    link = service.take_and_upload_screenshot()
    assert link == "https://drive.google.com/file/d/abc123/view"


def test_captures_fullscreen(service, capture):
    service.take_and_upload_screenshot()
    capture.capture_fullscreen.assert_called_once()


def test_generates_filename(service, capture):
    service.take_and_upload_screenshot()
    capture.generate_filename.assert_called_once()


def test_uploads_with_correct_args(service, capture, drive_client):
    service.take_and_upload_screenshot()
    drive_client.upload_and_share.assert_called_once_with(
        b"png_bytes", "screenshot_20260315_120000.png"
    )


def test_copies_link_to_clipboard(service, clipboard, drive_client):
    service.take_and_upload_screenshot()
    clipboard.copy.assert_called_once_with("https://drive.google.com/file/d/abc123/view")
