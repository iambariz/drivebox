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
            # Simulate pressing a key if on_press is provided
            if self.on_press:
                self.on_press("X")

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

    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")
    assert len(manager.registered_hotkeys) == 1

    triggered = []
    bridge.hotkey_activated.connect(lambda name: triggered.append(name))
    bridge.hotkey_activated.emit("fullscreen")

    assert "fullscreen" in triggered


def test_parse_hotkey():
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    keys = manager.parse_hotkey("Ctrl+Alt+X")
    assert len(keys) == 3  # ctrl, alt, and 'x'


def test_multiple_hotkeys(qtbot):
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    manager.register_hotkey("Ctrl+Alt+X", "fullscreen", "fullscreen")
    manager.register_hotkey("Ctrl+Shift+Q", "quit", "quit")

    assert len(manager.registered_hotkeys) == 2

def test_parse_hotkey_invalid_part():
    """Invalid parts should be ignored"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    keys = manager.parse_hotkey("Ctrl+Banana+Z")
    # "Banana" ignored, but Z parsed
    assert any(getattr(k, "char", None) == "z" for k in keys)


def test_parse_hotkey_single_letter():
    """Single key hotkey"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    keys = manager.parse_hotkey("X")
    assert any(getattr(k, "char", None) == "x" for k in keys)


def test_start_listener_no_hotkeys(monkeypatch):
    """start_listener should return early if no hotkeys registered"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    called = {"listener": False}

    def fake_listener(*args, **kwargs):
        called["listener"] = True

    monkeypatch.setattr("pynput.keyboard.Listener", fake_listener)

    manager.start_listener()
    assert called["listener"] is False


def test_start_listener_with_hotkey(monkeypatch, qtbot):
    """start_listener should emit signal when hotkey pressed"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    # Register a hotkey
    manager.registered_hotkeys = {frozenset(["X"]): ("fullscreen", "fullscreen")}

    triggered = []
    bridge.hotkey_activated.connect(lambda name: triggered.append(name))

    # Fake listener that calls on_press immediately
    class FakeListener:
        def __init__(self, on_press=None, on_release=None):
            self.on_press = on_press
            self.on_release = on_release
            self.daemon = True

        def start(self):
            if self.on_press:
                self.on_press("X")

        def stop(self):
            pass

    monkeypatch.setattr("pynput.keyboard.Listener", FakeListener)

    manager.start_listener()
    assert "fullscreen" in triggered


def test_start_listener_replaces_existing_listener(monkeypatch):
    """If listener already exists, it should be stopped and replaced"""
    bridge = DummyBridge()
    manager = HotkeyManager(bridge)

    manager.registered_hotkeys = {frozenset(["X"]): ("fullscreen", "fullscreen")}

    stopped = {"called": False}

    class FakeListener:
        def __init__(self, on_press=None, on_release=None):
            self.on_press = on_press
            self.on_release = on_release
            self.daemon = True

        def start(self):
            pass

        def stop(self):
            stopped["called"] = True

    monkeypatch.setattr("pynput.keyboard.Listener", FakeListener)

    # First listener
    manager.start_listener()
    # Second call should stop the first
    manager.start_listener()

    assert stopped["called"] is True