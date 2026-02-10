from PyQt5.QtWidgets import QApplication

from drivebox.ui.windows.main_window import MainWindow


def main() -> int:
    qt_app = QApplication([])
    window = MainWindow()
    window.show()
    exit_code: int = qt_app.exec_()
    return exit_code
