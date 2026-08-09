"""Bridges an async D-Bus portal Response signal to a blocking QEventLoop."""

from PyQt5.QtCore import QEventLoop, QObject, pyqtSlot
from PyQt5.QtDBus import QDBusMessage


class PortalResponseReceiver(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.response: int | None = None
        self.results: dict[str, object] = {}
        self.loop = QEventLoop()

    @pyqtSlot(QDBusMessage)
    def on_response(self, message: QDBusMessage) -> None:
        args = message.arguments()
        self.response = args[0]
        self.results = args[1]
        self.loop.quit()
