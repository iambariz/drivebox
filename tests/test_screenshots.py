import os
import pytest
from unittest.mock import patch, MagicMock
from drivebox.screenshots import ScreenshotService


def test_process_and_upload_success(tmp_path, monkeypatch):
    # Create a fake file
    fake_file = tmp_path / "screenshot.png"
    fake_file.write_text("dummy")

    notifier = MagicMock()

    service = ScreenshotService(notifier)

    # Patch upload_file_to_drivebox and pyperclip
    monkeypatch.setattr("drivebox.screenshots.upload_file_to_drivebox", lambda f: "http://link")
    monkeypatch.setattr("drivebox.screenshots.pyperclip.copy", lambda x: None)

    service.process_and_upload(str(fake_file), "Success", "Fail")

    notifier.notify.assert_called_with("Success", "Link copied to clipboard")
    # File should be deleted
    assert not fake_file.exists()


def test_process_and_upload_no_file(monkeypatch):
    notifier = MagicMock()
    service = ScreenshotService(notifier)

    service.process_and_upload("nonexistent.png", "Success", "Fail")

    notifier.notify.assert_called_with("Fail", "Could not capture screenshot")


def test_process_and_upload_upload_failure(tmp_path, monkeypatch):
    fake_file = tmp_path / "screenshot.png"
    fake_file.write_text("dummy")

    notifier = MagicMock()
    service = ScreenshotService(notifier)

    def fake_upload(_):
        raise RuntimeError("upload error")

    monkeypatch.setattr("drivebox.screenshots.upload_file_to_drivebox", fake_upload)
    monkeypatch.setattr("drivebox.screenshots.pyperclip.copy", lambda x: None)

    service.process_and_upload(str(fake_file), "Success", "Fail")

    notifier.notify.assert_called_with("Upload Failed", "upload error")
    # File should still exist because upload failed
    assert fake_file.exists()


def test_take_fullscreen(monkeypatch):
    notifier = MagicMock()
    service = ScreenshotService(notifier)

    # Patch Screenshotter.take_fullscreen
    monkeypatch.setattr(service.ss, "take_fullscreen", lambda: "fake.png")
    monkeypatch.setattr(service, "process_and_upload", MagicMock())

    service.take_fullscreen()

    service.process_and_upload.assert_called_with("fake.png", "Screenshot Uploaded", "Screenshot Failed")


def test_take_region(monkeypatch):
    notifier = MagicMock()
    service = ScreenshotService(notifier)

    monkeypatch.setattr(service.ss, "take_region", lambda: "region.png")
    monkeypatch.setattr(service, "process_and_upload", MagicMock())

    called = {"restart": False}
    def fake_restart():
        called["restart"] = True

    service.take_region(fake_restart)

    service.process_and_upload.assert_called_with("region.png", "Region Screenshot Uploaded", "Region Screenshot Failed")
    assert called["restart"] is True