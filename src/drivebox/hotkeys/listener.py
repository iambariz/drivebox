import logging
from functools import partial

from PyQt5.QtCore import QObject, pyqtSignal

from drivebox.actions import CaptureAction


try:
    from pynput import keyboard
except ImportError as e:  # pynput needs an X server on Linux, so pure Wayland sessions fail
    keyboard = None
    _keyboard_import_error: ImportError | None = e
else:
    _keyboard_import_error = None


logger = logging.getLogger(__name__)


class HotkeyListener(QObject):
    action_triggered = pyqtSignal(str)

    def __init__(self, actions: list[CaptureAction], parent=None) -> None:
        super().__init__(parent)
        self._actions = actions
        self._hotkeys = None
        if keyboard is None:
            logger.warning("Global hotkeys unavailable: %s", _keyboard_import_error)
            return
        self._hotkeys = keyboard.GlobalHotKeys(
            {action.hotkey: partial(self._on_hotkey, action) for action in actions}
        )

    @property
    def available(self) -> bool:
        return self._hotkeys is not None

    def start(self) -> None:
        if self._hotkeys is None:
            return
        self._hotkeys.start()
        hotkeys = ", ".join(f"{a.hotkey} ({a.label})" for a in self._actions)
        logger.info("Global hotkey listener started: %s", hotkeys)

    def stop(self) -> None:
        if self._hotkeys is not None:
            self._hotkeys.stop()

    def _on_hotkey(self, action: CaptureAction) -> None:
        logger.info("Hotkey %s triggered (%s)", action.hotkey, action.id)
        self.action_triggered.emit(action.id)
