"""Unit tests for HotkeyListener."""

from unittest.mock import MagicMock, patch

from PyQt5.QtCore import QCoreApplication

from drivebox.actions import CaptureAction
from drivebox.hotkeys import HotkeyListener


_app = QCoreApplication.instance() or QCoreApplication([])

ACTIONS = [CaptureAction(id="screenshot", label="Take Screenshot", hotkey="<ctrl>+<shift>+s")]


def test_listener_unavailable_without_keyboard_backend():
    with patch("drivebox.hotkeys.listener.keyboard", None):
        listener = HotkeyListener(actions=ACTIONS)

    assert listener.available is False
    listener.start()
    listener.stop()


def test_listener_registers_hotkeys_and_emits_action():
    keyboard = MagicMock()
    with patch("drivebox.hotkeys.listener.keyboard", keyboard):
        listener = HotkeyListener(actions=ACTIONS)

    assert listener.available is True
    bindings = keyboard.GlobalHotKeys.call_args.args[0]
    assert list(bindings) == ["<ctrl>+<shift>+s"]

    triggered = []
    listener.action_triggered.connect(triggered.append)
    bindings["<ctrl>+<shift>+s"]()

    assert triggered == ["screenshot"]
    listener.start()
    keyboard.GlobalHotKeys.return_value.start.assert_called_once()
