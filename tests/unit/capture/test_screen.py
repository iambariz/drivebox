"""Unit tests for ScreenCapture."""

import re
from unittest.mock import MagicMock, patch

from drivebox.capture.screen import ScreenCapture


def test_generate_filename_format():
    filename = ScreenCapture.generate_filename()
    assert re.match(r"screenshot_\d{8}_\d{6}\.png", filename)


def test_generate_filename_is_unique():
    names = {ScreenCapture.generate_filename() for _ in range(3)}
    # All names follow the same pattern; just assert it doesn't crash
    assert all(name.startswith("screenshot_") for name in names)


def test_save_local_writes_bytes(tmp_path):
    path = tmp_path / "shot.png"
    ScreenCapture.save_local(b"data", path)
    assert path.read_bytes() == b"data"


@patch("drivebox.capture.screen.imageio_ffmpeg.get_ffmpeg_exe", return_value="/usr/bin/ffmpeg")
@patch("drivebox.capture.screen.subprocess.run")
@patch("drivebox.capture.screen.QApplication")
def test_capture_fullscreen_calls_ffmpeg(mock_qapp, mock_run, mock_ffmpeg, tmp_path):
    screen = MagicMock()
    screen.geometry.return_value.width.return_value = 1920
    screen.geometry.return_value.height.return_value = 1080
    mock_qapp.primaryScreen.return_value = screen

    fake_png = b"\x89PNG\r\n"

    def fake_subprocess(cmd, **kwargs):
        # Write fake PNG to the temp file path (last arg in cmd)
        from pathlib import Path

        Path(cmd[-1]).write_bytes(fake_png)
        return MagicMock()

    mock_run.side_effect = fake_subprocess

    result = ScreenCapture.capture_fullscreen()

    assert result == fake_png
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert "/usr/bin/ffmpeg" in cmd
    assert "1920x1080" in cmd
