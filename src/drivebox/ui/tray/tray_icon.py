import logging
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

from drivebox.actions import CaptureAction


logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    action_triggered = pyqtSignal(str)

    def __init__(self, actions: list[CaptureAction], parent=None) -> None:
        # Load icon
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "logo_alt.png"
        icon = QIcon(str(icon_path))

        super().__init__(icon, parent)

        # Create menu
        self.menu = QMenu()

        # Add actions
        self.login_action = QAction("Login", self)
        self.show_action = QAction("Settings", self)
        self.quit_action = QAction("Quit", self)

        self.menu.addAction(self.login_action)
        self.menu.addAction(self.show_action)

        self.capture_actions: dict[str, QAction] = {}
        for action in actions:
            qaction = QAction(action.label, self)
            qaction.triggered.connect(self._make_emitter(action.id))
            self.menu.addAction(qaction)
            self.capture_actions[action.id] = qaction

        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self._on_activated)
        self.show()

    def _make_emitter(self, action_id: str):
        return lambda: self.action_triggered.emit(action_id)

    def set_authenticated(self, authenticated: bool) -> None:
        self.login_action.setVisible(not authenticated)
        self.show_action.setVisible(authenticated)
        for qaction in self.capture_actions.values():
            qaction.setVisible(authenticated)

    def _on_activated(self, reason):
        logger.info("On activated with reason: %s", reason)
