from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class HotkeyRecorderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Record Hotkey")
        self.setFixedSize(300, 150)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.instruction_label = QLabel("Press the key combination you want to use.\nPress ESC to cancel.")
        self.layout.addWidget(self.instruction_label)

        self.status_label = QLabel("Waiting for key press...")
        self.layout.addWidget(self.status_label)

        self.modifiers = set()
        self.main_key = None
        self.hotkey_result = None

        self.setFocusPolicy(Qt.StrongFocus)
        self.grabKeyboard()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.releaseKeyboard()
            self.reject()
            return

        # Track modifiers
        if event.key() == Qt.Key_Control:
            self.modifiers.add("Ctrl")
        elif event.key() == Qt.Key_Alt:
            self.modifiers.add("Alt")
        elif event.key() == Qt.Key_Shift:
            self.modifiers.add("Shift")
        elif event.key() == Qt.Key_Meta:
            self.modifiers.add("Super")
        else:
            # Only set main_key if it's not a modifier
            self.main_key = self._get_key_name(event)

        # Update display
        self.status_label.setText("Keys pressed: " + self._format_hotkey())

    def keyReleaseEvent(self, event):
        # If a non-modifier key is released, accept the combo
        if event.key() not in (Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta):
            if self.main_key:
                self.hotkey_result = self._format_hotkey()
                self.releaseKeyboard()
                self.accept()
        else:
            # Remove modifier from set
            if event.key() == Qt.Key_Control:
                self.modifiers.discard("Ctrl")
            elif event.key() == Qt.Key_Alt:
                self.modifiers.discard("Alt")
            elif event.key() == Qt.Key_Shift:
                self.modifiers.discard("Shift")
            elif event.key() == Qt.Key_Meta:
                self.modifiers.discard("Super")
            # Update display
            self.status_label.setText("Keys pressed: " + self._format_hotkey())

    def _get_key_name(self, event):
        # Try to get text representation first for printable characters
        text = event.text()

        # Handle all keys by their key code
        key = event.key()

        # Check for letter keys (Qt.Key_A through Qt.Key_Z)
        if Qt.Key_A <= key <= Qt.Key_Z:
            return chr(key)

        # Check for number keys
        if Qt.Key_0 <= key <= Qt.Key_9:
            return chr(key)

        # Other special keys
        key_mapping = {
            Qt.Key_F1: "F1", Qt.Key_F2: "F2", Qt.Key_F3: "F3", Qt.Key_F4: "F4",
            Qt.Key_F5: "F5", Qt.Key_F6: "F6", Qt.Key_F7: "F7", Qt.Key_F8: "F8",
            Qt.Key_F9: "F9", Qt.Key_F10: "F10", Qt.Key_F11: "F11", Qt.Key_F12: "F12",
            Qt.Key_Print: "Print", Qt.Key_Home: "Home", Qt.Key_End: "End",
            Qt.Key_Insert: "Insert", Qt.Key_Delete: "Delete", Qt.Key_PageUp: "PageUp",
            Qt.Key_PageDown: "PageDown", Qt.Key_Tab: "Tab", Qt.Key_Space: "Space",
            Qt.Key_Return: "Return", Qt.Key_Backspace: "Backspace",
            # Keyboard modifiers for future - it's working atm
        }
        return key_mapping.get(key, text.upper() if text.strip() else None)


    def _format_hotkey(self):
        # Show modifiers first, then main key
        if self.main_key:
            parts = list(self.modifiers)
            parts.sort(key=lambda k: {"Ctrl": 0, "Alt": 1, "Shift": 2, "Super": 3}.get(k, 99))
            parts.append(self.main_key)
            return "+".join(parts)
        else:
            return "+".join(sorted(self.modifiers))

    def closeEvent(self, event):
        self.releaseKeyboard()
        super().closeEvent(event)
