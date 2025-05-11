# ui/options_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox
)
from settings import load_settings, save_settings
from auth import get_gdrive_service, delete_token

def get_user_info(service):
    about = service.about().get(fields="user").execute()
    return about["user"]["displayName"], about["user"]["emailAddress"]

class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DriveBox Options")
        self.setFixedSize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.greeting_label = QLabel()
        self.signin_button = QPushButton("Sign in to Google Drive")
        self.logout_button = QPushButton("Log out")
        self.permission_label = QLabel("Who can view uploaded screenshots?")
        self.permission_dropdown = QComboBox()
        self.permission_dropdown.addItems([
            "Anyone with the link",
            "Only me"
        ])

        self.signin_button.clicked.connect(self.login_to_gdrive)
        self.logout_button.clicked.connect(self.logout)
        self.permission_dropdown.currentIndexChanged.connect(self.save_permission)

        self.layout.addWidget(self.greeting_label)
        self.layout.addWidget(self.signin_button)
        self.layout.addWidget(self.logout_button)
        self.layout.addWidget(self.permission_label)
        self.layout.addWidget(self.permission_dropdown)

        self.update_ui()

    def update_ui(self):
        settings = load_settings()
        user = settings.get("user")
        if user:
            first_name = user["name"].split()[0]
            self.greeting_label.setText(f"Hello, {first_name}!")
            self.signin_button.hide()
            self.logout_button.show()
            self.permission_label.show()
            self.permission_dropdown.show()
            # Set dropdown to current setting
            if settings.get("sharing", "anyone") == "anyone":
                self.permission_dropdown.setCurrentIndex(0)
            else:
                self.permission_dropdown.setCurrentIndex(1)
        else:
            self.greeting_label.setText("Please sign in to Google Drive.")
            self.signin_button.show()
            self.logout_button.hide()
            self.permission_label.hide()
            self.permission_dropdown.hide()

    def login_to_gdrive(self):
        service = get_gdrive_service()
        if service:
            name, email = get_user_info(service)
            settings = load_settings()
            settings["user"] = {"name": name, "email": email}
            save_settings(settings)
            self.update_ui()

    def logout(self):
        delete_token()
        settings = load_settings()
        settings["user"] = None
        save_settings(settings)
        self.update_ui()

    def save_permission(self):
        settings = load_settings()
        if self.permission_dropdown.currentIndex() == 0:
            settings["sharing"] = "anyone"
        else:
            settings["sharing"] = "private"
        save_settings(settings)
