from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QHBoxLayout, QInputDialog
)
from settings import load_settings, save_settings
from auth import get_gdrive_service, delete_token

def get_user_info(service):
    about = service.about().get(fields="user").execute()
    return about["user"]["displayName"], about["user"]["emailAddress"]

class OptionsWindow(QDialog):
    def __init__(self, hotkey_callback=None):
        super().__init__()
        self.setWindowTitle("DriveBox Options")
        self.setFixedSize(350, 250)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hotkey_callback = hotkey_callback  # Function to call when hotkey changes

        # Greeting and sign in/out
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

        # Hotkey section
        self.hotkey_label = QLabel("Screenshot shortcut:")
        self.hotkey_field = QLineEdit()
        self.hotkey_field.setReadOnly(True)
        self.change_hotkey_btn = QPushButton("Change")
        self.reset_hotkey_btn = QPushButton("Reset")

        hotkey_layout = QHBoxLayout()
        hotkey_layout.addWidget(self.hotkey_field)
        hotkey_layout.addWidget(self.change_hotkey_btn)
        hotkey_layout.addWidget(self.reset_hotkey_btn)

        self.layout.addWidget(self.hotkey_label)
        self.layout.addLayout(hotkey_layout)

        self.change_hotkey_btn.clicked.connect(self.change_hotkey)
        self.reset_hotkey_btn.clicked.connect(self.reset_hotkey)

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
        # Hotkey field
        self.hotkey_field.setText(settings.get("hotkey", "Ctrl+Alt+X"))

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

    def change_hotkey(self):
        new_hotkey, ok = QInputDialog.getText(self, "Change Hotkey", "Enter new hotkey (e.g., Ctrl+Shift+S):")
        if ok and new_hotkey:
            settings = load_settings()
            settings["hotkey"] = new_hotkey
            save_settings(settings)
            self.hotkey_field.setText(new_hotkey)
            if self.hotkey_callback:
                self.hotkey_callback(new_hotkey)

    def reset_hotkey(self):
        default_hotkey = "Ctrl+Alt+X"
        settings = load_settings()
        settings["hotkey"] = default_hotkey
        save_settings(settings)
        self.hotkey_field.setText(default_hotkey)
        if self.hotkey_callback:
            self.hotkey_callback(default_hotkey)

        settings = load_settings()
        if self.permission_dropdown.currentIndex() == 0:
            settings["sharing"] = "anyone"
        else:
            settings["sharing"] = "private"
        save_settings(settings)
