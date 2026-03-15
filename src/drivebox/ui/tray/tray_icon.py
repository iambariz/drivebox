import logging
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon


logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        # Load icon
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "logo_alt.png"
        icon = QIcon(str(icon_path))

        super().__init__(icon, parent)

        # Create menu
        self.menu = QMenu()

        # Add actions
        self.login_action = QAction("Login", self)
        self.show_action = QAction("Settings", self)
        self.screenshot_action = QAction("Take Screenshot", self)
        self.quit_action = QAction("Quit", self)

        self.menu.addAction(self.login_action)
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.screenshot_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self._on_activated)
        self.show()

    def set_authenticated(self, authenticated: bool) -> None:
        self.login_action.setVisible(not authenticated)
        self.show_action.setVisible(authenticated)
        self.screenshot_action.setVisible(authenticated)

    def _on_activated(self, reason):
        logger.info("On activated with reason: %s", reason)
