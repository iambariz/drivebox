import logging

from PyQt5.QtWidgets import QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from drivebox.auth import GoogleDriveAuthServiceFactory, delete_token


logger = logging.getLogger(__name__)


class AuthControls(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.auth_service = GoogleDriveAuthServiceFactory.create()
        self.greeting_label: QLabel
        self.signin_button: QPushButton
        self.logout_button: QPushButton
        self._setup_ui()
        self._update_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.greeting_label = QLabel()
        self.signin_button = QPushButton("Sign in to Google Drive")
        self.logout_button = QPushButton("Log out")

        layout.addWidget(self.greeting_label)
        layout.addWidget(self.signin_button)
        layout.addWidget(self.logout_button)

        self.signin_button.clicked.connect(self._handle_login)
        self.logout_button.clicked.connect(self._handle_logout)

    def _handle_login(self) -> None:
        try:
            # THIS OPENS THE BROWSER!
            self.auth_service.get_credentials()
            self._update_ui()
            QMessageBox.information(self, "Success", "Successfully authenticated!")
        except FileNotFoundError as e:
            QMessageBox.critical(
                self,
                "Credentials Missing",
                f"Could not find Google OAuth credentials.\n\n{e}",
            )
        except Exception as e:
            logger.exception("Login failed")
            QMessageBox.critical(self, "Error", f"Authentication failed: {e}")

    def _handle_logout(self) -> None:
        delete_token()
        self._update_ui()
        QMessageBox.information(self, "Logged Out", "Successfully logged out!")

    def _update_ui(self) -> None:
        token = self.auth_service.token_storage.load()
        is_authenticated = token is not None and token.valid

        if is_authenticated:
            self.greeting_label.setText("✓ Connected to Google Drive")
            self.signin_button.hide()
            self.logout_button.show()
        else:
            self.greeting_label.setText("Not connected")
            self.signin_button.show()
            self.logout_button.hide()
