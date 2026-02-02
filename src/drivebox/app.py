from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel


class App(QObject):
    started = pyqtSignal()

    def run(self) -> int:
        qtApp = QApplication([])
        label = QLabel("Drivebox is running")
        label.setMinimumWidth(300)
        label.show()

        self.started.emit()
        return qtApp.exec_()