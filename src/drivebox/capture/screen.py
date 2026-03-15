"""Screenshot capture functionality."""

import os
import subprocess  # nosec B404
import tempfile
from datetime import datetime
from pathlib import Path

import imageio_ffmpeg
from PyQt5.QtWidgets import QApplication


class ScreenCapture:
    @staticmethod
    def capture_fullscreen() -> bytes:
        """Capture full screen and return as PNG bytes via ffmpeg x11grab."""
        screen = QApplication.primaryScreen()
        geo = screen.geometry()
        size = f"{geo.width()}x{geo.height()}"
        display = os.environ.get("DISPLAY", ":0")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            tmp_path = Path(f.name)

        try:
            subprocess.run(  # nosec B603
                [
                    imageio_ffmpeg.get_ffmpeg_exe(),
                    "-y",
                    "-f",
                    "x11grab",
                    "-video_size",
                    size,
                    "-i",
                    display,
                    "-vframes",
                    "1",
                    str(tmp_path),
                ],
                check=True,
                capture_output=True,
            )
            return tmp_path.read_bytes()
        finally:
            tmp_path.unlink(missing_ok=True)

    @staticmethod
    def generate_filename() -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot_{timestamp}.png"

    @staticmethod
    def save_local(image_data: bytes, path: Path) -> None:
        """Save screenshot to local file."""
        path.write_bytes(image_data)
