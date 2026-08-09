"""Fullscreen capture via Qt's screen grab (X11 Linux, Windows, macOS)."""

from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtWidgets import QApplication

from drivebox.capture.base import Capturer


class QScreenCapturer(Capturer):
    def capture_fullscreen(self) -> bytes:
        screen = QApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("No primary screen available")
        pixmap = screen.grabWindow(0)  # type: ignore[arg-type]

        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)  # type: ignore[attr-defined]
        pixmap.save(buffer, "PNG")
        return bytes(buffer.data())
