import os
import sys
import subprocess
from unittest.mock import patch, MagicMock
import drivebox.screen_recorder as sr
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

def test_get_ffmpeg_path_exists(tmp_path, monkeypatch):
    fake_ffmpeg = tmp_path / "ffmpeg"
    fake_ffmpeg.write_text("binary")

    monkeypatch.setattr(sr, "resource_path", lambda p: str(fake_ffmpeg))
    monkeypatch.setattr(sys, "platform", "linux")

    recorder = ScreenRecorder()
    path = recorder._get_ffmpeg_path()
    assert path == str(fake_ffmpeg)


def test_get_ffmpeg_path_missing(monkeypatch):
    monkeypatch.setattr(sr, "resource_path", lambda p: "/nonexistent/ffmpeg")
    monkeypatch.setattr(sys, "platform", "linux")

    recorder = ScreenRecorder()
    path = recorder._get_ffmpeg_path()
    assert path == "ffmpeg"


def test_list_pulse_devices_success(monkeypatch):
    fake_result = MagicMock()
    fake_result.stdout = (
        "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor\n"
        "alsa_input.pci-0000_00_1b.0.analog-stereo"
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: fake_result)

    recorder = ScreenRecorder()
    recorder.ffmpeg_path = "ffmpeg"
    devices = recorder._list_pulse_devices()
    assert "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor" in devices


def test_list_pulse_devices_failure(monkeypatch):
    monkeypatch.setattr(
        subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail"))
    )

    recorder = ScreenRecorder()
    recorder.ffmpeg_path = "ffmpeg"
    devices = recorder._list_pulse_devices()
    assert devices == []


def test_get_default_audio_args_linux_monitor(monkeypatch):
    recorder = ScreenRecorder()
    recorder._list_pulse_devices = lambda: ["alsa_output.monitor"]
    monkeypatch.setattr(sys, "platform", "linux")
    args = recorder._get_default_audio_args()
    assert "alsa_output.monitor" in args


def test_get_default_audio_args_linux_mic(monkeypatch):
    recorder = ScreenRecorder()
    recorder._list_pulse_devices = lambda: ["alsa_input.mic"]
    monkeypatch.setattr(sys, "platform", "linux")
    args = recorder._get_default_audio_args()
    assert "alsa_input.mic" in args


def test_get_default_audio_args_linux_none(monkeypatch):
    recorder = ScreenRecorder()
    recorder._list_pulse_devices = lambda: []
    monkeypatch.setattr(sys, "platform", "linux")
    args = recorder._get_default_audio_args()
    assert args == []


def test_get_default_audio_args_darwin(monkeypatch):
    recorder = ScreenRecorder()
    monkeypatch.setattr(sys, "platform", "darwin")
    args = recorder._get_default_audio_args()
    assert "avfoundation" in args


def test_get_default_audio_args_win32(monkeypatch):
    recorder = ScreenRecorder()
    monkeypatch.setattr(sys, "platform", "win32")
    args = recorder._get_default_audio_args()
    assert "dshow" in args


def test_get_default_audio_args_unknown(monkeypatch):
    recorder = ScreenRecorder()
    monkeypatch.setattr(sys, "platform", "unknown")
    args = recorder._get_default_audio_args()
    assert args == []


def test_start_recording_success(monkeypatch):
    fake_proc = MagicMock()
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: fake_proc)
    monkeypatch.setattr(sys, "platform", "linux")

    recorder = ScreenRecorder()
    recorder.ffmpeg_path = "ffmpeg"
    recorder.start_recording()
    assert recorder.process == fake_proc
    assert recorder.output_file.endswith(".mp4")


def test_start_recording_failure(monkeypatch):
    monkeypatch.setattr(
        subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(Exception("fail"))
    )
    monkeypatch.setattr(sys, "platform", "linux")

    recorder = ScreenRecorder()
    recorder.ffmpeg_path = "ffmpeg"
    recorder.start_recording()
    assert recorder.process is None


def test_stop_recording_success(tmp_path):
    fake_file = tmp_path / "recording.mp4"
    fake_file.write_text("data")

    fake_proc = MagicMock()
    fake_proc.wait = lambda timeout=5: None

    recorder = ScreenRecorder()
    recorder.process = fake_proc
    recorder.output_file = str(fake_file)

    result = recorder.stop_recording()
    assert result == str(fake_file)
    fake_proc.terminate.assert_called_once()


def test_stop_recording_file_missing(tmp_path):
    fake_proc = MagicMock()
    fake_proc.wait = lambda timeout=5: None

    recorder = ScreenRecorder()
    recorder.process = fake_proc
    recorder.output_file = str(tmp_path / "missing.mp4")

    result = recorder.stop_recording()
    assert result is None


def test_stop_recording_no_process():
    recorder = ScreenRecorder()
    recorder.process = None
    assert recorder.stop_recording() is None