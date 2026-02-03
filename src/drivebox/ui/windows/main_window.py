from PyQt5.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Drivebox")
        self.setMinimumSize(600, 400)

        label = QLabel("Drivebox is running", self)
        label.move(20, 20)
