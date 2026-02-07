from PyQt5.QtWidgets import QApplication

from drivebox.ui.windows.main_window import MainWindow


def main() -> None:
    qt_app = QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(qtApp.exec_())
