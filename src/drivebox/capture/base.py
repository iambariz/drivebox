"""Capturer interface and shared utilities."""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class Capturer(ABC):
    @abstractmethod
    def capture_fullscreen(self) -> bytes:
        """Capture full screen and return as PNG bytes."""


def generate_filename() -> str:
    """Generate timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"screenshot_{timestamp}.png"


def save_local(image_data: bytes, path: Path) -> None:
    """Save screenshot to local file."""
    path.write_bytes(image_data)
