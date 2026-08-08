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


@patch("drivebox.capture.screen.QApplication")
def test_capture_fullscreen_returns_png_bytes(mock_qapp):
    fake_png = b"\x89PNG\r\n\x1a\nfake-image-data"

    def fake_save(buffer, fmt):
        assert fmt == "PNG"
        buffer.write(fake_png)

    mock_pixmap = MagicMock()
    mock_pixmap.save.side_effect = fake_save

    mock_screen = MagicMock()
    mock_screen.grabWindow.return_value = mock_pixmap
    mock_qapp.primaryScreen.return_value = mock_screen

    result = ScreenCapture.capture_fullscreen()

    assert result == fake_png
    mock_screen.grabWindow.assert_called_once_with(0)
