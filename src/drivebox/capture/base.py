"""Capturer interface and shared utilities."""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class Capturer(ABC):
    @abstractmethod
    def capture_fullscreen(self) -> bytes:
        """Capture full screen and return as PNG bytes."""

    @abstractmethod
    def capture_region(self) -> bytes | None:
        """Capture a user-selected region. Returns None if the user cancels."""


def generate_filename(prefix: str = "screenshot") -> str:
    """Generate timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.png"


def save_local(image_data: bytes, path: Path) -> None:
    """Save screenshot to local file."""
    path.write_bytes(image_data)
