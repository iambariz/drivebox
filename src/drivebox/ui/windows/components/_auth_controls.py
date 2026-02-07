from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class AuthControls(QWidget):
    """Authentication section with greeting and signin/logout buttons."""

    def __init__(self) -> None:
        super().__init__()
        self.greeting_label: QLabel
        self.signin_button: QPushButton
        self.logout_button: QPushButton
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create UI elements."""
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
        """Handle login button click."""
        print("Login button clicked")

    def _handle_logout(self) -> None:
        """Handle logout button click."""
        print("Logout button clicked")

    def update_ui(self) -> None:
        """Update UI based on authentication state."""
        print("Updating UI based on auth state")
