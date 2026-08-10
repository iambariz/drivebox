"""Unit tests for QScreenCapturer."""

from unittest.mock import MagicMock, patch

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QDialog

from drivebox.capture import QScreenCapturer


def _mock_pixmap(fake_png: bytes) -> MagicMock:
    def fake_save(buffer, fmt):
        assert fmt == "PNG"
        buffer.write(fake_png)

    mock_pixmap = MagicMock()
    mock_pixmap.save.side_effect = fake_save
    return mock_pixmap


@patch("drivebox.capture.qscreen_capturer.QApplication")
def test_capture_fullscreen_returns_png_bytes(mock_qapp):
    fake_png = b"\x89PNG\r\n\x1a\nfake-image-data"
    mock_pixmap = _mock_pixmap(fake_png)

    mock_screen = MagicMock()
    mock_screen.grabWindow.return_value = mock_pixmap
    mock_qapp.primaryScreen.return_value = mock_screen

    result = QScreenCapturer().capture_fullscreen()

    assert result == fake_png
    mock_screen.grabWindow.assert_called_once_with(0)


@patch("drivebox.capture.qscreen_capturer.RegionSelector")
@patch("drivebox.capture.qscreen_capturer.QApplication")
def test_capture_region_returns_cropped_png_bytes(mock_qapp, mock_region_selector):
    fake_png = b"\x89PNG\r\n\x1a\nfake-region-data"
    rect = QRect(10, 10, 100, 100)

    full_pixmap = MagicMock()
    cropped_pixmap = _mock_pixmap(fake_png)
    full_pixmap.copy.return_value = cropped_pixmap

    mock_screen = MagicMock()
    mock_screen.grabWindow.return_value = full_pixmap
    mock_qapp.primaryScreen.return_value = mock_screen

    mock_selector = MagicMock()
    mock_selector.exec_.return_value = QDialog.Accepted
    mock_selector.selected_rect = rect
    mock_region_selector.return_value = mock_selector

    result = QScreenCapturer().capture_region()

    assert result == fake_png
    full_pixmap.copy.assert_called_once_with(rect)


@patch("drivebox.capture.qscreen_capturer.RegionSelector")
@patch("drivebox.capture.qscreen_capturer.QApplication")
def test_capture_region_returns_none_on_cancel(mock_qapp, mock_region_selector):
    mock_screen = MagicMock()
    mock_screen.grabWindow.return_value = MagicMock()
    mock_qapp.primaryScreen.return_value = mock_screen

    mock_selector = MagicMock()
    mock_selector.exec_.return_value = QDialog.Rejected
    mock_selector.selected_rect = None
    mock_region_selector.return_value = mock_selector

    result = QScreenCapturer().capture_region()

    assert result is None
