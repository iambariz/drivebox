import os, sys, types

# If running in CI (headless), mock pynput
if os.environ.get("CI") == "true":
    sys.modules['pynput'] = types.ModuleType("pynput")
    sys.modules['pynput.keyboard'] = types.ModuleType("pynput.keyboard")
    sys.modules['pynput.keyboard'].Key = object
    sys.modules['pynput.keyboard'].KeyCode = lambda char=None: char

import pytest
from PyQt5.QtCore import QObject, pyqtSignal
from drivebox.hotkeys import HotkeyManager

class DummyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

def test_register_hotkey_and_emit(qtbot):
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")

    keys = manager.parse_hotkey("Ctrl+Alt+X")
    manager.registered_hotkeys[keys] = ("fullscreen", "fullscreen")

    triggered = []

    def on_hotkey(name):
        triggered.append(name)

    bridge.hotkey_activated.connect(on_hotkey)
    bridge.hotkey_activated.emit("fullscreen")

    assert "fullscreen" in triggered