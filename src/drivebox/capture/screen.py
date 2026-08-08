"""Screenshot capture functionality."""

from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtWidgets import QApplication


class ScreenCapture:
    @staticmethod
    def capture_fullscreen() -> bytes:
        """Capture full screen and return as PNG bytes via Qt's screen grab."""
        screen = QApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("No primary screen available")
        pixmap = screen.grabWindow(0)  # type: ignore[arg-type]

        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)  # type: ignore[attr-defined]
        pixmap.save(buffer, "PNG")
        return bytes(buffer.data())

    @staticmethod
    def generate_filename() -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot_{timestamp}.png"

    @staticmethod
    def save_local(image_data: bytes, path: Path) -> None:
        """Save screenshot to local file."""
        path.write_bytes(image_data)
