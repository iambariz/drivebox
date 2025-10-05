import os
import pytest
from unittest.mock import MagicMock, patch
from drivebox.recording import RecordingService


def test__do_start_success(monkeypatch):
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.start_recording.return_value = None

        service = RecordingService(notifier, upload_func, app_state)

        # Act
        service._do_start()

        # Assert
        assert service.is_recording is True
        notifier.notify.assert_called_with("Screen Recording", "Recording started")


def test__do_start_failure(monkeypatch):
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.start_recording.side_effect = Exception("fail")

        service = RecordingService(notifier, upload_func, app_state)

        with pytest.raises(Exception) as exc:
            service._do_start()

        assert "fail" in str(exc.value)
        assert service.is_recording is False
        notifier.notify.assert_called_with("Screen Recording Failed", "fail")


def test__do_stop_and_upload_success(tmp_path, monkeypatch):
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    # Create a temp output file to simulate recording result
    output = tmp_path / "recording.mp4"
    output.write_text("data")

    # Stub pyperclip
    monkeypatch.setattr("drivebox.recording.pyperclip.copy", lambda x: None)

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.stop_recording.return_value = str(output)

        upload_func.return_value = "http://link"

        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = True  # simulate active recording

        # Act
        link = service._do_stop_and_upload()

        # Assert
        assert link == "http://link"
        assert service.is_recording is False
        upload_func.assert_called_once_with(str(output))
        notifier.notify.assert_called_with(
            "Recording Uploaded", "Link copied to clipboard"
        )


def test__do_stop_and_upload_no_file(monkeypatch):
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        # Return a path that doesn't exist
        mock_recorder.stop_recording.return_value = "nonexistent.mp4"

        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = True

        with pytest.raises(RuntimeError) as exc:
            service._do_stop_and_upload()

        assert "No recording file found" in str(exc.value)
        assert service.is_recording is False
        notifier.notify.assert_called_with("Recording Failed", "No recording file found.")


def test__do_stop_and_upload_upload_failure(tmp_path, monkeypatch):
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    output = tmp_path / "recording.mp4"
    output.write_text("data")

    monkeypatch.setattr("drivebox.recording.pyperclip.copy", lambda x: None)

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.stop_recording.return_value = str(output)

        upload_func.side_effect = RuntimeError("upload error")

        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = True

        with pytest.raises(RuntimeError) as exc:
            service._do_stop_and_upload()

        assert "upload error" in str(exc.value)
        assert service.is_recording is False
        notifier.notify.assert_called_with("Recording Failed", "upload error")


def test_start_recording_enqueues_when_not_recording():
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder"):
        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = False

        service.start_recording()

    # Should enqueue worker and notify queued
    app_state.enqueue.assert_called_once()
    args, kwargs = app_state.enqueue.call_args
    assert args[0].__func__ is service._do_start.__func__
    assert args[0].__self__ is service
    assert kwargs == {}
    notifier.notify.assert_called_with("Queued Task", "Recording start queued")


def test_start_recording_already_recording():
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder"):
        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = True

        service.start_recording()

    # Should not enqueue, just notify
    app_state.enqueue.assert_not_called()
    notifier.notify.assert_called_with("Screen Recording", "Already recording")


def test_stop_and_upload_enqueues_when_recording():
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder"):
        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = True

        service.stop_and_upload()

    app_state.enqueue.assert_called_once()
    args, kwargs = app_state.enqueue.call_args
    assert args[0].__func__ is service._do_stop_and_upload.__func__
    assert args[0].__self__ is service    
    assert kwargs == {}
    notifier.notify.assert_called_with("Queued Task", "Recording stop+upload queued")


def test_stop_and_upload_when_not_recording():
    notifier = MagicMock()
    upload_func = MagicMock()
    app_state = MagicMock()

    with patch("drivebox.recording.ScreenRecorder"):
        service = RecordingService(notifier, upload_func, app_state)
        service.is_recording = False

        service.stop_and_upload()

    app_state.enqueue.assert_not_called()
    notifier.notify.assert_called_with("Screen Recording", "Not currently recording")