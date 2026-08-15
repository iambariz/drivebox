"""Unit tests for WaylandPortalCapturer."""

from unittest.mock import MagicMock, patch

from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtDBus import QDBusMessage

from drivebox.capture import WaylandPortalCapturer


_app = QCoreApplication.instance() or QCoreApplication([])


@patch("drivebox.capture.wayland_portal_capturer.QDBusInterface")
@patch("drivebox.capture.wayland_portal_capturer.QDBusConnection")
def test_capture_fullscreen_returns_png_bytes(mock_dbus_connection, mock_dbus_interface, tmp_path):
    fake_png = b"\x89PNG\r\n\x1a\nfake-image-data"
    screenshot_path = tmp_path / "screenshot.png"
    screenshot_path.write_bytes(fake_png)

    mock_bus = MagicMock()
    mock_bus.isConnected.return_value = True
    mock_dbus_connection.sessionBus.return_value = mock_bus

    mock_reply = MagicMock()
    mock_reply.type.return_value = QDBusMessage.ReplyMessage
    mock_reply.arguments.return_value = ["/org/freedesktop/portal/desktop/request/1_1/t"]
    mock_dbus_interface.return_value.call.return_value = mock_reply

    def fake_connect(service, path, interface, name, slot):
        message = MagicMock()
        message.arguments.return_value = [0, {"uri": f"file://{screenshot_path}"}]
        QTimer.singleShot(0, lambda: slot(message))
        return True

    mock_bus.connect.side_effect = fake_connect

    result = WaylandPortalCapturer().capture_fullscreen()

    assert result == fake_png
    assert not screenshot_path.exists()


@patch("drivebox.capture.wayland_portal_capturer.QDBusInterface")
@patch("drivebox.capture.wayland_portal_capturer.QDBusConnection")
def test_capture_region_returns_png_bytes(mock_dbus_connection, mock_dbus_interface, tmp_path):
    fake_png = b"\x89PNG\r\n\x1a\nfake-region-data"
    screenshot_path = tmp_path / "region.png"
    screenshot_path.write_bytes(fake_png)

    mock_bus = MagicMock()
    mock_bus.isConnected.return_value = True
    mock_dbus_connection.sessionBus.return_value = mock_bus

    mock_reply = MagicMock()
    mock_reply.type.return_value = QDBusMessage.ReplyMessage
    mock_reply.arguments.return_value = ["/org/freedesktop/portal/desktop/request/1_2/t"]
    mock_dbus_interface.return_value.call.return_value = mock_reply

    call_options = {}

    def fake_call(method, parent_window, options):
        call_options.update(options)
        return mock_reply

    mock_dbus_interface.return_value.call.side_effect = fake_call

    def fake_connect(service, path, interface, name, slot):
        message = MagicMock()
        message.arguments.return_value = [0, {"uri": f"file://{screenshot_path}"}]
        QTimer.singleShot(0, lambda: slot(message))
        return True

    mock_bus.connect.side_effect = fake_connect

    result = WaylandPortalCapturer().capture_region()

    assert result == fake_png
    assert call_options == {"interactive": True}


@patch("drivebox.capture.wayland_portal_capturer.QDBusInterface")
@patch("drivebox.capture.wayland_portal_capturer.QDBusConnection")
def test_capture_region_returns_none_on_cancel(mock_dbus_connection, mock_dbus_interface):
    mock_bus = MagicMock()
    mock_bus.isConnected.return_value = True
    mock_dbus_connection.sessionBus.return_value = mock_bus

    mock_reply = MagicMock()
    mock_reply.type.return_value = QDBusMessage.ReplyMessage
    mock_reply.arguments.return_value = ["/org/freedesktop/portal/desktop/request/1_3/t"]
    mock_dbus_interface.return_value.call.return_value = mock_reply

    def fake_connect(service, path, interface, name, slot):
        message = MagicMock()
        message.arguments.return_value = [1, {}]  # cancelled
        QTimer.singleShot(0, lambda: slot(message))
        return True

    mock_bus.connect.side_effect = fake_connect

    result = WaylandPortalCapturer().capture_region()

    assert result is None
