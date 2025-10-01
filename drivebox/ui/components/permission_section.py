from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox


class PermissionSection(QWidget):
    """Permission/sharing settings dropdown."""
    
    SHARING_OPTIONS = {
        0: ("Anyone with the link", "anyone"),
        1: ("Only me", "private")
    }
    
    def __init__(self, settings_repo):
        super().__init__()
        self.settings_repo = settings_repo
        
        self._setup_ui()
        self.update_ui()
    
    def _setup_ui(self):
        """Create UI elements."""
        layout = QVBoxLayout(self)
        
        self.label = QLabel("Who can view uploaded screenshots?")
        self.dropdown = QComboBox()
        self.dropdown.addItems([opt[0] for opt in self.SHARING_OPTIONS.values()])
        
        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)
        
        self.dropdown.currentIndexChanged.connect(self._handle_change)
    
    def _handle_change(self):
        """Handle dropdown selection change."""
        index = self.dropdown.currentIndex()
        mode = self.SHARING_OPTIONS[index][1]
        self.settings_repo.set_sharing_mode(mode)
    
    def update_ui(self):
        """Update visibility and selection based on auth state."""
        user = self.settings_repo.get_user()
        visible = user is not None
        self.label.setVisible(visible)
        self.dropdown.setVisible(visible)
        
        if visible:
            mode = self.settings_repo.get_sharing_mode()
            for idx, (_, value) in self.SHARING_OPTIONS.items():
                if value == mode:
                    self.dropdown.setCurrentIndex(idx)
                    break
