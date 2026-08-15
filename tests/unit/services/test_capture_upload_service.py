"""Unit tests for CaptureUploadService."""

from unittest.mock import MagicMock, patch

from PyQt5.QtCore import QCoreApplication, QEventLoop, QTimer

from drivebox.services import CaptureUploadService


_app = QCoreApplication.instance() or QCoreApplication([])


def _wait_for_signal(signal, timeout_ms=3000):
    loop = QEventLoop()
    result = {}

    def on_signal(value):
        result["value"] = value
        loop.quit()

    signal.connect(on_signal)
    QTimer.singleShot(timeout_ms, loop.quit)
    loop.exec_()
    return result.get("value")


@patch("drivebox.services.capture_upload_service.ClipboardManager")
@patch("drivebox.services.capture_upload_service.DriveClient")
@patch("drivebox.services.capture_upload_service.get_gdrive_service")
@patch("drivebox.services.capture_upload_service.get_capturer")
def test_capture_fullscreen_emits_upload_finished(
    mock_get_capturer, mock_get_gdrive_service, mock_drive_client_cls, mock_clipboard_cls
):
    mock_capturer = MagicMock()
    mock_capturer.capture_fullscreen.return_value = b"png_bytes"
    mock_get_capturer.return_value = mock_capturer
    mock_drive_client_cls.return_value.upload_and_share.return_value = (
        "https://drive.google.com/file/d/abc123/view"
    )

    service = CaptureUploadService()
    service.capture_fullscreen()

    link = _wait_for_signal(service.upload_finished)

    assert link == "https://drive.google.com/file/d/abc123/view"
    mock_drive_client_cls.return_value.upload_and_share.assert_called_once()
    mock_clipboard_cls.return_value.copy.assert_called_once_with(link)


@patch("drivebox.services.capture_upload_service.get_capturer")
def test_capture_fullscreen_emits_upload_failed_on_capture_error(mock_get_capturer):
    mock_capturer = MagicMock()
    mock_capturer.capture_fullscreen.side_effect = RuntimeError("boom")
    mock_get_capturer.return_value = mock_capturer

    service = CaptureUploadService()
    errors = []
    service.upload_failed.connect(errors.append)

    service.capture_fullscreen()

    assert errors == ["Screenshot capture failed"]


@patch("drivebox.services.capture_upload_service.get_capturer")
def test_capture_region_cancelled_emits_nothing(mock_get_capturer):
    mock_capturer = MagicMock()
    mock_capturer.capture_region.return_value = None
    mock_get_capturer.return_value = mock_capturer

    service = CaptureUploadService()
    finished = []
    failed = []
    service.upload_finished.connect(finished.append)
    service.upload_failed.connect(failed.append)

    service.capture_region()

    assert finished == []
    assert failed == []


@patch("drivebox.services.capture_upload_service.ClipboardManager")
@patch("drivebox.services.capture_upload_service.DriveClient")
@patch("drivebox.services.capture_upload_service.get_gdrive_service")
@patch("drivebox.services.capture_upload_service.get_capturer")
def test_upload_failure_wraps_error_message(
    mock_get_capturer, mock_get_gdrive_service, mock_drive_client_cls, mock_clipboard_cls
):
    mock_capturer = MagicMock()
    mock_capturer.capture_region.return_value = b"png_bytes"
    mock_get_capturer.return_value = mock_capturer
    mock_drive_client_cls.return_value.upload_and_share.side_effect = RuntimeError("network down")

    service = CaptureUploadService()
    service.capture_region()

    error = _wait_for_signal(service.upload_failed)

    assert error == "Upload failed: network down"
