from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QTabWidget, QLabel, QPushButton, QComboBox,
    QLineEdit, QHBoxLayout, QMessageBox
)
from datetime import datetime

from drivebox.settings import load_settings, save_settings
from drivebox.auth import get_gdrive_service, delete_token
from drivebox.ui.options_hotkey_recorder import HotkeyRecorderDialog
from drivebox.ui.hotkeys_manager import HotkeysManager


def get_user_info(service):
    about = service.about().get(fields="user").execute()
    return about["user"]["displayName"], about["user"]["emailAddress"]


class OptionsWindow(QDialog):
    def __init__(self, hotkey_callback=None):
        super().__init__()
        self.setWindowTitle("DriveBox")
        self.setFixedSize(600, 500)

        vbox = QVBoxLayout(self)
        self.tabs = QTabWidget()
        vbox.addWidget(self.tabs)

        # -------------------- Log Tab --------------------
        self.log_tab = QWidget()
        self.log_layout = QVBoxLayout(self.log_tab)
        self.log_table = QTableWidget(0, 4)
        self.log_table.setHorizontalHeaderLabels(["Time", "Type", "Status", "Result"])
        self.log_layout.addWidget(self.log_table)
        self.tabs.addTab(self.log_tab, "📜 Log")

        # -------------------- Settings Tab --------------------
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.tabs.addTab(self.settings_tab, "⚙ Settings")

        self.hotkey_callback = hotkey_callback
        self.hotkey_manager = HotkeysManager()
        self.hotkey_fields = {}

        # Greeting + signin/logout
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

        self.settings_layout.addWidget(self.greeting_label)
        self.settings_layout.addWidget(self.signin_button)
        self.settings_layout.addWidget(self.logout_button)
        self.settings_layout.addWidget(self.permission_label)
        self.settings_layout.addWidget(self.permission_dropdown)

        # Hotkey section (dynamic)
        hotkeys_title = QLabel("Hotkey Shortcuts:")
        self.settings_layout.addWidget(hotkeys_title)

        for action, (label_text, default) in self.hotkey_manager.DEFAULTS.items():
            self._add_hotkey_row(action, label_text, default)

        self.update_ui()

        # Default: show Log tab first
        self.tabs.setCurrentIndex(0)

    # -------------------- Log Helpers --------------------
    def add_log_entry(self, event_type, status, result=""):
        row = self.log_table.rowCount()
        self.log_table.insertRow(row)
        self.log_table.setItem(row, 0, QTableWidgetItem(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.log_table.setItem(row, 1, QTableWidgetItem(event_type))
        self.log_table.setItem(row, 2, QTableWidgetItem(status))
        self.log_table.setItem(row, 3, QTableWidgetItem(result))

    # -------------------- Settings UI Builders --------------------
    def _add_hotkey_row(self, action, label_text, default):
        label = QLabel(f"{label_text}:")
        field = QLineEdit()
        field.setReadOnly(True)
        field.setText(self.hotkey_manager.get(action))

        change_btn = QPushButton("Change")
        reset_btn = QPushButton("Reset")

        row = QHBoxLayout()
        row.addWidget(label)
        row.addWidget(field)
        row.addWidget(change_btn)
        row.addWidget(reset_btn)

        self.settings_layout.addLayout(row)
        self.hotkey_fields[action] = field

        change_btn.clicked.connect(lambda _, act=action, fld=field: self.change_hotkey(act, fld))
        reset_btn.clicked.connect(lambda _, act=action, fld=field, d=default: self.reset_hotkey(act, fld, d))

    # -------------------- Auth and UI --------------------
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

        # Update hotkeys
        for action, field in self.hotkey_fields.items():
            field.setText(self.hotkey_manager.get(action))

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

    # -------------------- Hotkey Logic --------------------
    def change_hotkey(self, action, field):
        dialog = HotkeyRecorderDialog(self)
        if dialog.exec_():
            new_hotkey = dialog.hotkey_result
            if new_hotkey:
                try:
                    self.hotkey_manager.set(action, new_hotkey)
                except ValueError as e:
                    QMessageBox.warning(self, "Duplicate Hotkey", str(e))
                    return
                field.setText(new_hotkey)
                if self.hotkey_callback:
                    self.hotkey_callback(action, new_hotkey)

    def reset_hotkey(self, action, field, default_value):
        self.hotkey_manager.reset(action)
        field.setText(self.hotkey_manager.get(action))
        if self.hotkey_callback:
            self.hotkey_callback(action, self.hotkey_manager.get(action))