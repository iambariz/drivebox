from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class AuthSection(QWidget):
    """Authentication section with greeting and signin/logout buttons."""
    
    def __init__(self, auth_service, settings_repo):
        super().__init__()
        self.auth_service = auth_service
        self.settings_repo = settings_repo
        
        self._setup_ui()
        self.update_ui()
    
    def _setup_ui(self):
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
    
    def _handle_login(self):
        """Handle login button click."""
        user_info = self.auth_service.login()
        if user_info:
            self.settings_repo.set_user(user_info)
            self.update_ui()
    
    def _handle_logout(self):
        """Handle logout button click."""
        self.auth_service.logout()
        self.settings_repo.set_user(None)
        self.update_ui()
    
    def update_ui(self):
        """Update UI based on authentication state."""
        user = self.settings_repo.get_user()
        if user:
            first_name = user["name"].split()[0]
            self.greeting_label.setText(f"Hello, {first_name}!")
            self.signin_button.hide()
            self.logout_button.show()
        else:
            self.greeting_label.setText("Please sign in to Google Drive.")
            self.signin_button.show()
            self.logout_button.hide()
