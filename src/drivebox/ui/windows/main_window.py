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
        self.tray_icon.show_action.triggered.connect(self.show_window)
        self.tray_icon.screenshot_action.triggered.connect(self._take_screenshot)
        self.tray_icon.quit_action.triggered.connect(self.quit_app)

        # Handle tray icon click
        self.tray_icon.activated.connect(self.on_tray_activated)

    def close_event(self, event):
        """Minimize to tray instead of closing"""
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
        """Handle tray icon click"""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_window()

    def _take_screenshot(self):
        self.auth_controls._take_screenshot()

    def quit_app(self):
        """Actually quit the app"""
        self.tray_icon.hide()
        QApplication.quit()
