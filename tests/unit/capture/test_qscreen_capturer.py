"""Unit tests for QScreenCapturer."""

from unittest.mock import MagicMock, patch

from drivebox.capture import QScreenCapturer


@patch("drivebox.capture.qscreen_capturer.QApplication")
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

    result = QScreenCapturer().capture_fullscreen()

    assert result == fake_png
    mock_screen.grabWindow.assert_called_once_with(0)
