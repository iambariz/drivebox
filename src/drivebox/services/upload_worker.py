import logging
from collections.abc import Callable

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

from drivebox.clipboard import ClipboardManager
from drivebox.drive import DriveClient


logger = logging.getLogger(__name__)


class UploadJobSignals(QObject):
    finished = pyqtSignal(str)
    failed = pyqtSignal(str)


class UploadJob(QRunnable):
    def __init__(
        self,
        image_data: bytes,
        filename: str,
        drive_client_factory: Callable[[], DriveClient],
        clipboard: ClipboardManager,
    ) -> None:
        super().__init__()
        self.image_data = image_data
        self.filename = filename
        self.drive_client_factory = drive_client_factory
        self.clipboard = clipboard
        self.signals = UploadJobSignals()

    def run(self) -> None:
        try:
            # Built here so token refresh or re-authentication stays off the UI thread
            drive_client = self.drive_client_factory()
            link = drive_client.upload_and_share(self.image_data, self.filename)
            self.clipboard.copy(link)
        except Exception as e:
            logger.exception("Upload failed")
            self.signals.failed.emit(str(e))
        else:
            self.signals.finished.emit(link)
