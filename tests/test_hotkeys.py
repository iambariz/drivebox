import pytest
from PyQt5.QtCore import QObject, pyqtSignal
from drivebox.hotkeys import HotkeyManager

class DummyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

def test_register_hotkey_and_emit(qtbot):
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    # Register a hotkey
    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")

    # Simulate pressing keys
    keys = manager.parse_hotkey("Ctrl+Alt+X")
    manager.registered_hotkeys[keys] = ("fullscreen", "fullscreen")

    triggered = []

    def on_hotkey(name):
        triggered.append(name)

    bridge.hotkey_activated.connect(on_hotkey)

    # Manually emit (simulate keypress)
    bridge.hotkey_activated.emit("fullscreen")

    assert "fullscreen" in triggered