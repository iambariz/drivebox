"""Unit tests for ScreenshotService."""

from unittest.mock import MagicMock, patch

import pytest

from drivebox.services.screenshot_service import ScreenshotService


@pytest.fixture
def capture():
    mock = MagicMock()
    mock.capture_fullscreen.return_value = b"png_bytes"
    mock.capture_region.return_value = b"region_png_bytes"
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


@patch(
    "drivebox.services.screenshot_service.generate_filename",
    return_value="screenshot_20260315_120000.png",
)
def test_uploads_with_correct_args(mock_generate_filename, service, drive_client):
    service.take_and_upload_screenshot()
    drive_client.upload_and_share.assert_called_once_with(
        b"png_bytes", "screenshot_20260315_120000.png"
    )


def test_copies_link_to_clipboard(service, clipboard, drive_client):
    service.take_and_upload_screenshot()
    clipboard.copy.assert_called_once_with("https://drive.google.com/file/d/abc123/view")


@patch(
    "drivebox.services.screenshot_service.generate_filename",
    return_value="region_20260315_120000.png",
)
def test_region_uploads_with_correct_args(mock_generate_filename, service, drive_client):
    link = service.take_and_upload_region()

    mock_generate_filename.assert_called_once_with("region")
    drive_client.upload_and_share.assert_called_once_with(
        b"region_png_bytes", "region_20260315_120000.png"
    )
    assert link == "https://drive.google.com/file/d/abc123/view"


def test_region_cancelled_skips_upload_and_clipboard(service, capture, drive_client, clipboard):
    capture.capture_region.return_value = None

    link = service.take_and_upload_region()

    assert link is None
    drive_client.upload_and_share.assert_not_called()
    clipboard.copy.assert_not_called()
