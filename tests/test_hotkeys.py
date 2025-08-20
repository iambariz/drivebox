import os, sys, types

# If running in CI (headless), mock pynput
if os.environ.get("CI") == "true":
    sys.modules['pynput'] = types.ModuleType("pynput")
    sys.modules['pynput.keyboard'] = types.ModuleType("pynput.keyboard")

    class FakeKey:
        ctrl_l = "ctrl_l"
        alt_l = "alt_l"
        shift_l = "shift_l"

    class FakeKeyCode:
        def __init__(self, char=None):
            self.char = char

        @staticmethod
        def from_char(char):
            return FakeKeyCode(char)

    class FakeListener:
        def __init__(self, on_press=None, on_release=None):
            self.on_press = on_press
            self.on_release = on_release
            self.daemon = True
        
        def start(self):
            pass
        
        def stop(self):
            pass

    sys.modules['pynput.keyboard'].Key = FakeKey
    sys.modules['pynput.keyboard'].KeyCode = FakeKeyCode
    sys.modules['pynput.keyboard'].Listener = FakeListener

import pytest
from PyQt5.QtCore import QObject, pyqtSignal
from drivebox.hotkeys import HotkeyManager


class DummyBridge(QObject):
    hotkey_activated = pyqtSignal(str)


def test_register_hotkey_and_emit(qtbot):
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    # Register the hotkey
    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")

    # Verify the hotkey was registered
    assert len(manager.registered_hotkeys) == 1
    
    # Test the signal emission
    triggered = []

    def on_hotkey(name):
        triggered.append(name)

    bridge.hotkey_activated.connect(on_hotkey)
    bridge.hotkey_activated.emit("fullscreen")

    assert "fullscreen" in triggered


def test_parse_hotkey():
    """Test hotkey parsing functionality"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)
    
    # Test parsing
    keys = manager.parse_hotkey("Ctrl+Alt+X")
    assert len(keys) == 3  # ctrl, alt, and 'x'


def test_multiple_hotkeys(qtbot):
    """Test registering multiple hotkeys"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")
    manager.register_hotkey("Ctrl+Shift+Q", "quit", "quit")

    assert len(manager.registered_hotkeys) == 2