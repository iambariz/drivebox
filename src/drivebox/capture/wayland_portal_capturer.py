"""Fullscreen and region capture via the xdg-desktop-portal Screenshot API (Wayland)."""

from pathlib import Path
from urllib.parse import unquote, urlparse

from PyQt5.QtCore import QTimer
from PyQt5.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage

from drivebox.capture.base import Capturer
from drivebox.capture.portal_response_receiver import PortalResponseReceiver


PORTAL_SERVICE = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
PORTAL_SCREENSHOT_IFACE = "org.freedesktop.portal.Screenshot"
PORTAL_REQUEST_IFACE = "org.freedesktop.portal.Request"
PORTAL_TIMEOUT_MS = 10_000
PORTAL_RESPONSE_SUCCESS = 0
PORTAL_RESPONSE_CANCELLED = 1


class WaylandPortalCapturer(Capturer):
    def capture_fullscreen(self) -> bytes:
        data = self._capture(interactive=False)
        if data is None:
            raise RuntimeError("Screenshot portal request was cancelled unexpectedly")
        return data

    def capture_region(self) -> bytes | None:
        return self._capture(interactive=True)

    def _capture(self, interactive: bool) -> bytes | None:
        bus = QDBusConnection.sessionBus()
        if not bus.isConnected():
            raise RuntimeError("Could not connect to D-Bus session bus")

        interface = QDBusInterface(PORTAL_SERVICE, PORTAL_PATH, PORTAL_SCREENSHOT_IFACE, bus)
        reply = interface.call("Screenshot", "", {"interactive": interactive})
        if reply.type() == QDBusMessage.ErrorMessage:
            raise RuntimeError(f"Portal Screenshot call failed: {reply.errorMessage()}")

        handle = reply.arguments()[0]

        receiver = PortalResponseReceiver()
        connected = bus.connect(
            PORTAL_SERVICE, handle, PORTAL_REQUEST_IFACE, "Response", receiver.on_response
        )
        if not connected:
            raise RuntimeError("Could not connect to portal Response signal")

        QTimer.singleShot(PORTAL_TIMEOUT_MS, receiver.loop.quit)
        receiver.loop.exec_()

        if receiver.response is None:
            raise RuntimeError("Timed out waiting for screenshot portal response")
        if receiver.response == PORTAL_RESPONSE_CANCELLED:
            return None
        if receiver.response != PORTAL_RESPONSE_SUCCESS:
            raise RuntimeError(f"Screenshot portal request failed (code {receiver.response})")

        uri = receiver.results.get("uri")
        if not uri:
            raise RuntimeError("Screenshot portal response missing 'uri'")

        path = Path(unquote(urlparse(str(uri)).path))
        try:
            return path.read_bytes()
        finally:
            path.unlink(missing_ok=True)
