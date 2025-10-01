from typing import Optional, Callable
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from .hotkey_row import HotkeyRow


class HotkeysSection(QWidget):
    """Collection of hotkey configuration rows."""
    
    def __init__(self, hotkey_manager, on_change: Optional[Callable] = None):
        super().__init__()
        self.hotkey_manager = hotkey_manager
        self.hotkey_rows = []
        
        self._setup_ui(on_change)
    
    def _setup_ui(self, on_change: Optional[Callable]):
        """Create title and hotkey rows."""
        layout = QVBoxLayout(self)
        
        title = QLabel("Hotkey Shortcuts:")
        layout.addWidget(title)
        
        for action, (label_text, default) in self.hotkey_manager.DEFAULTS.items():
            row = HotkeyRow(action, label_text, default, 
                          self.hotkey_manager, on_change)
            layout.addWidget(row)
            self.hotkey_rows.append(row)
    
    def update_ui(self):
        """Refresh all hotkey displays."""
        for row in self.hotkey_rows:
            row.update_display()
