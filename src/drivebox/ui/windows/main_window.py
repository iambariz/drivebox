from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from .components import AuthControls

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Drivebox")
        self.setMinimumSize(600, 400)

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Add the auth controls
        self.auth_controls = AuthControls()
        layout.addWidget(self.auth_controls)