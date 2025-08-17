from unittest.mock import patch, MagicMock
from drivebox.recording import RecordingService

def test_start_recording_success():
    notifier = MagicMock()
    upload_func = MagicMock()
    service = RecordingService(notifier, upload_func)

    with patch.object(service.recorder, "start_recording", return_value=None):
        service.start_recording()

    notifier.notify.assert_called_with("Screen Recording", "Recording started")

def test_start_recording_failure():
    notifier = MagicMock()
    upload_func = MagicMock()
    service = RecordingService(notifier, upload_func)

    with patch.object(service.recorder, "start_recording", side_effect=Exception("fail")):
        service.start_recording()

    notifier.notify.assert_called_with("Screen Recording Failed", "fail")