from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QVBoxLayout, QWidget

from drivebox.ui.tray.tray_icon import TrayIcon

from .components import AuthControls


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Drivebox")
        self.setMinimumSize(600, 400)

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add the auth controls
        self.auth_controls = AuthControls()
        layout.addWidget(self.auth_controls)

        # Tray icon
        self.tray_icon = TrayIcon(self)
        self.tray_icon.login_action.triggered.connect(self.auth_controls._handle_login)
        self.tray_icon.show_action.triggered.connect(self.show_window)
        self.tray_icon.screenshot_action.triggered.connect(self._take_screenshot)
        self.tray_icon.quit_action.triggered.connect(self.quit_app)

        self.auth_controls.auth_state_changed.connect(self.tray_icon.set_authenticated)
        self.auth_controls._update_ui()  # sync tray to current auth state

        self.tray_icon.activated.connect(self.on_tray_activated)

    def closeEvent(self, event):  # noqa: N802
        """Minimize to tray instead of closing."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Drivebox", "App minimized to tray", QSystemTrayIcon.Information, 2000
        )

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            # Standard platforms (Windows/macOS)
            self.show_window()
            return

        if reason == QSystemTrayIcon.Trigger:
            # Left-click: on Ubuntu/GNOME the context menu doesn't auto-show on
            # left-click, so we pop it up manually at the current cursor position.
            self.tray_icon.contextMenu().popup(QCursor.pos())

    def _take_screenshot(self):
        self.auth_controls._take_screenshot()

    def quit_app(self):
        """Actually quit the app."""
        self.tray_icon.hide()
        QApplication.quit()
