"""Screenshot capture functionality."""

import io
from datetime import datetime
from pathlib import Path

from PIL import ImageGrab


class ScreenCapture:
    @staticmethod
    def capture_fullscreen() -> bytes:
        """Capture full screen and return as PNG bytes."""
        screenshot = ImageGrab.grab()

        # Convert to PNG bytes
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return img_bytes.getvalue()

    @staticmethod
    def generate_filename() -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"screenshot_{timestamp}.png"

    @staticmethod
    def save_local(image_data: bytes, path: Path) -> None:
        """Save screenshot to local file."""
        with path.open("wb") as f:
            f.write(image_data)
