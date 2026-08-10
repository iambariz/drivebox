"""Fullscreen and region capture via Qt's screen grab (X11 Linux, Windows, macOS)."""

from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog

from drivebox.capture.base import Capturer
from drivebox.capture.region_selector import RegionSelector


class QScreenCapturer(Capturer):
    def capture_fullscreen(self) -> bytes:
        return self._pixmap_to_png(self._grab_screen())

    def capture_region(self) -> bytes | None:
        full_pixmap = self._grab_screen()

        selector = RegionSelector(full_pixmap)
        if selector.exec_() != QDialog.Accepted or selector.selected_rect is None:
            return None

        cropped = full_pixmap.copy(selector.selected_rect)
        return self._pixmap_to_png(cropped)

    def _grab_screen(self) -> QPixmap:
        screen = QApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("No primary screen available")
        return screen.grabWindow(0)  # type: ignore[arg-type]

    def _pixmap_to_png(self, pixmap: QPixmap) -> bytes:
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)  # type: ignore[attr-defined]
        pixmap.save(buffer, "PNG")
        return bytes(buffer.data())
