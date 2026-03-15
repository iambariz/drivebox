import logging

from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


logger = logging.getLogger(__name__)


class HotkeyListener(QObject):
    screenshot_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hotkeys = keyboard.GlobalHotKeys({"<ctrl>+<shift>+s": self._on_screenshot_hotkey})

    def start(self) -> None:
        self._hotkeys.start()
        logger.info("Global hotkey listener started (Ctrl+Shift+S)")

    def stop(self) -> None:
        self._hotkeys.stop()

    def _on_screenshot_hotkey(self) -> None:
        logger.info("Hotkey Ctrl+Shift+S triggered")
        self.screenshot_requested.emit()
