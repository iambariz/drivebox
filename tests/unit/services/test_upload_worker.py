"""Unit tests for UploadJob."""

from unittest.mock import MagicMock

from PyQt5.QtCore import QCoreApplication

from drivebox.services import UploadJob


_app = QCoreApplication.instance() or QCoreApplication([])


def test_run_emits_finished_with_link():
    drive_client = MagicMock()
    drive_client.upload_and_share.return_value = "https://drive.google.com/file/d/abc123/view"
    clipboard = MagicMock()

    job = UploadJob(b"png_bytes", "screenshot_20260315_120000.png", drive_client, clipboard)

    finished_links = []
    failed_errors = []
    job.signals.finished.connect(finished_links.append)
    job.signals.failed.connect(failed_errors.append)

    job.run()

    drive_client.upload_and_share.assert_called_once_with(
        b"png_bytes", "screenshot_20260315_120000.png"
    )
    clipboard.copy.assert_called_once_with("https://drive.google.com/file/d/abc123/view")
    assert finished_links == ["https://drive.google.com/file/d/abc123/view"]
    assert failed_errors == []


def test_run_emits_failed_on_upload_error():
    drive_client = MagicMock()
    drive_client.upload_and_share.side_effect = RuntimeError("upload failed")
    clipboard = MagicMock()

    job = UploadJob(b"png_bytes", "screenshot_20260315_120000.png", drive_client, clipboard)

    finished_links = []
    failed_errors = []
    job.signals.finished.connect(finished_links.append)
    job.signals.failed.connect(failed_errors.append)

    job.run()

    clipboard.copy.assert_not_called()
    assert finished_links == []
    assert failed_errors == ["upload failed"]
