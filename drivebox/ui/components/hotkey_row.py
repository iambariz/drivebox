from typing import Optional, Callable
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from drivebox.ui.options_hotkey_recorder import HotkeyRecorderDialog


class HotkeyRow(QWidget):
    """Single hotkey configuration with change and reset buttons."""
    
    def __init__(self, action: str, label_text: str, default: str,
                 hotkey_manager, on_change: Optional[Callable] = None):
        super().__init__()
        self.action = action
        self.default = default
        self.hotkey_manager = hotkey_manager
        self.on_change = on_change
        
        self._setup_ui(label_text)
    
    def _setup_ui(self, label_text: str):
        """Create UI elements."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(f"{label_text}:")
        self.field = QLineEdit()
        self.field.setReadOnly(True)
        self.field.setText(self.hotkey_manager.get(self.action))
        
        change_btn = QPushButton("Change")
        reset_btn = QPushButton("Reset")
        
        layout.addWidget(label)
        layout.addWidget(self.field)
        layout.addWidget(change_btn)
        layout.addWidget(reset_btn)
        
        change_btn.clicked.connect(self._handle_change)
        reset_btn.clicked.connect(self._handle_reset)
    
    def _handle_change(self):
        """Open dialog to record new hotkey."""
        dialog = HotkeyRecorderDialog(self)
        if dialog.exec_():
            new_hotkey = dialog.hotkey_result
            if new_hotkey:
                try:
                    self.hotkey_manager.set(self.action, new_hotkey)
                    self.field.setText(new_hotkey)
                    if self.on_change:
                        self.on_change(self.action, new_hotkey)
                except ValueError as e:
                    QMessageBox.warning(self, "Duplicate Hotkey", str(e))
    
    def _handle_reset(self):
        """Reset hotkey to default value."""
        self.hotkey_manager.reset(self.action)
        new_value = self.hotkey_manager.get(self.action)
        self.field.setText(new_value)
        if self.on_change:
            self.on_change(self.action, new_value)
    
    def update_display(self):
        """Refresh displayed hotkey value."""
        self.field.setText(self.hotkey_manager.get(self.action))