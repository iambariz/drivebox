"""Screen capture module."""

from .base import Capturer, generate_filename, save_local
from .factory import get_capturer, is_wayland
from .qscreen_capturer import QScreenCapturer
from .wayland_portal_capturer import WaylandPortalCapturer


__all__ = [
    "Capturer",
    "QScreenCapturer",
    "WaylandPortalCapturer",
    "generate_filename",
    "get_capturer",
    "is_wayland",
    "save_local",
]
