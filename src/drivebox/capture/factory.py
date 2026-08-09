"""Selects the right Capturer for the current session."""

import os

from drivebox.capture.base import Capturer
from drivebox.capture.qscreen_capturer import QScreenCapturer
from drivebox.capture.wayland_portal_capturer import WaylandPortalCapturer


def is_wayland() -> bool:
    return os.environ.get("XDG_SESSION_TYPE") == "wayland" or bool(
        os.environ.get("WAYLAND_DISPLAY")
    )


def get_capturer() -> Capturer:
    """Return the Capturer implementation for the current session."""
    if is_wayland():
        return WaylandPortalCapturer()
    return QScreenCapturer()
