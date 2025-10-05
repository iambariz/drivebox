import os
import pytest
from unittest.mock import MagicMock
from drivebox.screenshots import ScreenshotService


def test__process_and_upload_success(tmp_path, monkeypatch):
    # Arrange: create a real temp file
    fake_file = tmp_path / "screenshot.png"
    fake_file.write_text("dummy")

    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    # Patch upload and pyperclip
    monkeypatch.setattr(
        "drivebox.screenshots.upload_file_to_drivebox",
        lambda f: "http://link",
    )
    monkeypatch.setattr("drivebox.screenshots.pyperclip.copy", lambda x: None)

    # Act
    link = service._process_and_upload(
        str(fake_file), "Success", "Fail"
    )

    # Assert
    assert link == "http://link"
    notifier.notify.assert_called_with("Success", "Link copied to clipboard")
    assert not fake_file.exists()  # file deleted after successful upload


def test__process_and_upload_no_file(monkeypatch):
    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    # Act + Assert
    with pytest.raises(RuntimeError) as exc:
        service._process_and_upload(
            "nonexistent.png", "Success", "Fail"
        )
    assert "Screenshot capture failed" in str(exc.value)
    notifier.notify.assert_called_with("Fail", "Could not capture screenshot")


def test__process_and_upload_upload_failure(tmp_path, monkeypatch):
    fake_file = tmp_path / "screenshot.png"
    fake_file.write_text("dummy")

    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    def fake_upload(_):
        raise RuntimeError("upload error")

    monkeypatch.setattr(
        "drivebox.screenshots.upload_file_to_drivebox",
        fake_upload,
    )
    monkeypatch.setattr("drivebox.screenshots.pyperclip.copy", lambda x: None)

    with pytest.raises(RuntimeError) as exc:
        service._process_and_upload(
            str(fake_file), "Success", "Fail"
        )

    assert "upload error" in str(exc.value)
    notifier.notify.assert_called_with("Upload Failed", "upload error")
    # File should remain since upload failed
    assert fake_file.exists()


def test_take_fullscreen_enqueues_and_notifies(monkeypatch):
    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    # make ss.take_fullscreen return a path
    monkeypatch.setattr(service.ss, "take_fullscreen", lambda: "fake.png")

    # Act
    service.take_fullscreen()

    # Assert enqueue call
    app_state.enqueue.assert_called_once()
    # Validate args to enqueue: (callable, filename, success, fail)
    args, kwargs = app_state.enqueue.call_args
    assert args[0].__func__ is service._process_and_upload.__func__
    assert args[0].__self__ is service
    assert args[1] == "fake.png"
    assert args[2] == "Screenshot Uploaded"
    assert args[3] == "Screenshot Failed"
    assert kwargs == {}

    # Assert queued notification
    notifier.notify.assert_called_with(
        "Queued Task", "Fullscreen screenshot queued"
    )


def test_take_region_enqueues_notifies_and_restarts(monkeypatch):
    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    # make ss.take_region return a path
    monkeypatch.setattr(service.ss, "take_region", lambda: "region.png")

    called = {"restart": False}

    def fake_restart():
        called["restart"] = True

    # Act
    service.take_region(fake_restart)

    # Assert enqueue call
    app_state.enqueue.assert_called_once()
    args, kwargs = app_state.enqueue.call_args
    assert args[0].__func__ is service._process_and_upload.__func__
    assert args[0].__self__ is service
    assert args[1] == "region.png"
    assert args[2] == "Region Screenshot Uploaded"
    assert args[3] == "Region Screenshot Failed"
    assert kwargs == {}

    # Assert queued notification
    notifier.notify.assert_called_with(
        "Queued Task", "Region screenshot queued"
    )

    # Restart callback must be called
    assert called["restart"] is True


def test_take_region_restarts_on_exception(monkeypatch):
    notifier = MagicMock()
    app_state = MagicMock()
    service = ScreenshotService(notifier, app_state)

    # Simulate failure during region capture
    def raise_err():
        raise RuntimeError("capture failed")

    monkeypatch.setattr(service.ss, "take_region", raise_err)

    called = {"restart": False}

    def fake_restart():
        called["restart"] = True

    # Act: exception should not escape take_region; it should still call restart
    # The method itself doesn't catch exceptions from take_region except via finally,
    # so we expect the exception to propagate, but restart should still have been called.
    with pytest.raises(RuntimeError):
        service.take_region(fake_restart)

    assert called["restart"] is True
    # enqueue should not be called due to capture error
    app_state.enqueue.assert_not_called()