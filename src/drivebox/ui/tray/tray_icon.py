import logging
from pathlib import Path

from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon


logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        # Load icon
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "tray_icon.png"
        icon = QIcon(str(icon_path))

        super().__init__(icon, parent)

        # Create menu
        self.menu = QMenu()

        # Add actions
        self.show_action = QAction("Show Window", self)
        self.screenshot_action = QAction("Take Screenshot", self)
        self.quit_action = QAction("Quit", self)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.screenshot_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self._on_activated)
        self.show()

    def _on_activated(self, reason):
        logger = logging.getLogger(__name__)

        logger.info("On activated...")
        logger.info(reason)
        if reason == QSystemTrayIcon.Context:
            self.menu.popup(QCursor.pos())
