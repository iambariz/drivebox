import logging
from functools import partial

from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal

from drivebox.actions import CaptureAction


logger = logging.getLogger(__name__)


class HotkeyListener(QObject):
    action_triggered = pyqtSignal(str)

    def __init__(self, actions: list[CaptureAction], parent=None) -> None:
        super().__init__(parent)
        self._actions = actions
        self._hotkeys = keyboard.GlobalHotKeys(
            {action.hotkey: partial(self._on_hotkey, action) for action in actions}
        )

    def start(self) -> None:
        self._hotkeys.start()
        hotkeys = ", ".join(f"{a.hotkey} ({a.label})" for a in self._actions)
        logger.info("Global hotkey listener started: %s", hotkeys)

    def stop(self) -> None:
        self._hotkeys.stop()

    def _on_hotkey(self, action: CaptureAction) -> None:
        logger.info("Hotkey %s triggered (%s)", action.hotkey, action.id)
        self.action_triggered.emit(action.id)
