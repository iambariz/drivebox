from unittest.mock import patch, MagicMock
from drivebox.screen_recorder import ScreenRecorder

def test_start_and_stop_recording(tmp_path):
    recorder = ScreenRecorder()
    fake_process = MagicMock()
    fake_process.wait.return_value = 0

    with patch("drivebox.screen_recorder.subprocess.Popen", return_value=fake_process):
        recorder.start_recording()
        assert recorder.process is not None

        # Simulate stop
        recorder.output_file = str(tmp_path / "test.mp4")
        (tmp_path / "test.mp4").write_text("fake video")
        result = recorder.stop_recording()

    assert result.endswith("test.mp4")