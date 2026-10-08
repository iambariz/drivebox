"""Authentication UI controls."""

from PyQt5.QtCore import QThreadPool, pyqtSignal
from PyQt5.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from drivebox.auth import GoogleDriveAuthServiceFactory, delete_token
from drivebox.services import CaptureUploadService, LoginJob


class AuthControls(QWidget):
    auth_state_changed = pyqtSignal(bool)  # True = logged in

    def __init__(self) -> None:
        super().__init__()
        self.auth_service = GoogleDriveAuthServiceFactory.create()
        self.greeting_label: QLabel
        self.signin_button: QPushButton
        self.logout_button: QPushButton
        self.screenshot_button: QPushButton
        self.region_button: QPushButton
        self._login_pool = QThreadPool()
        self._login_pool.setMaxThreadCount(1)
        self._login_in_progress = False
        self._capture_service = CaptureUploadService()
        self._capture_service.upload_finished.connect(self._on_upload_finished)
        self._capture_service.upload_failed.connect(self._on_upload_failed)
        self._setup_ui()
        self._update_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.greeting_label = QLabel()
        self.signin_button = QPushButton("Sign in to Google Drive")
        self.logout_button = QPushButton("Log out")
        self.screenshot_button = QPushButton("Take Screenshot (Ctrl+Shift+S)")
        self.region_button = QPushButton("Capture Region (Ctrl+Shift+R)")

        layout.addWidget(self.greeting_label)
        layout.addWidget(self.signin_button)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.screenshot_button)
        layout.addWidget(self.region_button)

        self.signin_button.clicked.connect(self._handle_login)
        self.logout_button.clicked.connect(self._handle_logout)
        self.screenshot_button.clicked.connect(self._take_screenshot)
        self.region_button.clicked.connect(self._take_region_screenshot)

    def _handle_login(self) -> None:
        if self._login_in_progress:
            return
        self._login_in_progress = True
        self.signin_button.setEnabled(False)
        self.greeting_label.setText("Waiting for sign-in in your browser...")

        job = LoginJob(self.auth_service)
        job.signals.succeeded.connect(self._on_login_succeeded)
        job.signals.failed.connect(self._on_login_failed)
        self._login_pool.start(job)

    def _on_login_succeeded(self) -> None:
        self._finish_login()
        QMessageBox.information(self, "Success", "Successfully authenticated!")

    def _on_login_failed(self, error: str) -> None:
        self._finish_login()
        QMessageBox.critical(self, "Sign-in Failed", error)

    def _finish_login(self) -> None:
        self._login_in_progress = False
        self.signin_button.setEnabled(True)
        self._update_ui()

    def _handle_logout(self) -> None:
        delete_token()
        self._update_ui()
        QMessageBox.information(self, "Logged Out", "Successfully logged out!")

    def _take_screenshot(self) -> None:
        self._capture_service.capture_fullscreen()

    def _take_region_screenshot(self) -> None:
        self._capture_service.capture_region()

    def _on_upload_finished(self, link: str) -> None:
        QMessageBox.information(self, "Screenshot Uploaded!", f"Link copied to clipboard:\n{link}")

    def _on_upload_failed(self, error: str) -> None:
        QMessageBox.critical(self, "Error", error)

    def _update_ui(self) -> None:
        is_authenticated = self.auth_service.has_session()

        if is_authenticated:
            self.greeting_label.setText("✓ Connected to Google Drive")
            self.signin_button.hide()
            self.logout_button.show()
            self.screenshot_button.show()
            self.region_button.show()
        else:
            self.greeting_label.setText("Not connected")
            self.signin_button.show()
            self.logout_button.hide()
            self.screenshot_button.hide()
            self.region_button.hide()

        self.auth_state_changed.emit(is_authenticated)
