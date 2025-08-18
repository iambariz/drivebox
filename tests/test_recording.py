from unittest.mock import patch, MagicMock
from drivebox.recording import RecordingService

def test_start_recording_success():
    notifier = MagicMock()
    upload_func = MagicMock()

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.start_recording.return_value = None

        service = RecordingService(notifier, upload_func)
        service.start_recording()

    notifier.notify.assert_called_with("Screen Recording", "Recording started")

def test_start_recording_failure():
    notifier = MagicMock()
    upload_func = MagicMock()

    with patch("drivebox.recording.ScreenRecorder") as MockRecorder:
        mock_recorder = MockRecorder.return_value
        mock_recorder.start_recording.side_effect = Exception("fail")

        service = RecordingService(notifier, upload_func)
        service.start_recording()

    notifier.notify.assert_called_with("Screen Recording Failed", "fail")