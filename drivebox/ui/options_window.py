from typing import Optional, Callable
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QWidget, QTabWidget
)

from drivebox.services import GoogleDriveAuthService, SettingsRepository
from drivebox.ui.components import (
    LogTableWidget, AuthSection, PermissionSection, HotkeysSection
)
from drivebox.ui.hotkeys_manager import HotkeysManager


class OptionsWindow(QDialog):
    """Main options dialog with log and settings tabs."""
    
    def __init__(self, hotkey_callback: Optional[Callable] = None,
                 auth_service=None, settings_repo=None):
        """
        Args:
            hotkey_callback: Called when hotkeys change (action, new_value)
            auth_service: Optional auth service for testing
            settings_repo: Optional settings repo for testing
        """
        super().__init__()
        
        # Dependency injection with defaults
        self.auth_service = auth_service or GoogleDriveAuthService()
        self.settings_repo = settings_repo or SettingsRepository()
        self.hotkey_manager = HotkeysManager()
        
        self._setup_window()
        self._setup_tabs(hotkey_callback)
    
    def _setup_window(self):
        """Initialize window properties."""
        self.setWindowTitle("DriveBox")
        self.setFixedSize(600, 500)
        
        vbox = QVBoxLayout(self)
        self.tabs = QTabWidget()
        vbox.addWidget(self.tabs)
    
    def _setup_tabs(self, hotkey_callback: Optional[Callable]):
        """Create log and settings tabs."""
        self._setup_log_tab()
        self._setup_settings_tab(hotkey_callback)
        
        # Default to Log tab
        self.tabs.setCurrentIndex(0)
    
    def _setup_log_tab(self):
        """Create log tab with table."""
        self.log_tab = QWidget()
        layout = QVBoxLayout(self.log_tab)
        self.log_table = LogTableWidget()
        layout.addWidget(self.log_table)
        self.tabs.addTab(self.log_tab, "📜 Log")
    
    def _setup_settings_tab(self, hotkey_callback: Optional[Callable]):
        """Create settings tab with all sections."""
        self.settings_tab = QWidget()
        layout = QVBoxLayout(self.settings_tab)
        
        # Auth section
        self.auth_section = AuthSection(self.auth_service, self.settings_repo)
        layout.addWidget(self.auth_section)
        
        # Permission section
        self.permission_section = PermissionSection(self.settings_repo)
        layout.addWidget(self.permission_section)
        
        # Hotkeys section
        self.hotkeys_section = HotkeysSection(self.hotkey_manager, hotkey_callback)
        layout.addWidget(self.hotkeys_section)
        
        layout.addStretch()
        self.tabs.addTab(self.settings_tab, "⚙ Settings")
    
    # Public API
    def add_log_entry(self, event_type: str, status: str, result: str = ""):
        """Add entry to log table."""
        self.log_table.add_entry(event_type, status, result)
    
    def update_ui(self):
        """Refresh all UI components."""
        self.auth_section.update_ui()
        self.permission_section.update_ui()
        self.hotkeys_section.update_ui()