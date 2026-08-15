import logging

from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal

from drivebox.auth import get_gdrive_service
from drivebox.capture import generate_filename, get_capturer
from drivebox.clipboard import ClipboardManager
from drivebox.drive import DriveClient
from drivebox.services.upload_worker import UploadJob


logger = logging.getLogger(__name__)


class CaptureUploadService(QObject):
    upload_finished = pyqtSignal(str)
    upload_failed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._upload_pool = QThreadPool()
        self._upload_pool.setMaxThreadCount(1)

    def capture_fullscreen(self) -> None:
        self._capture_and_upload(
            get_capturer().capture_fullscreen, "screenshot", "Screenshot capture"
        )

    def capture_region(self) -> None:
        self._capture_and_upload(get_capturer().capture_region, "region", "Region capture")

    def _capture_and_upload(self, capture_fn, filename_prefix: str, error_label: str) -> None:
        try:
            image_data = capture_fn()
        except Exception:
            logger.exception(f"{error_label} failed")
            self.upload_failed.emit(f"{error_label} failed")
            return
        if image_data is None:
            return
        self._enqueue_upload(image_data, generate_filename(filename_prefix))

    def _enqueue_upload(self, image_data: bytes, filename: str) -> None:
        drive_service = get_gdrive_service()
        job = UploadJob(image_data, filename, DriveClient(drive_service), ClipboardManager())
        job.signals.finished.connect(self.upload_finished)
        job.signals.failed.connect(lambda err: self.upload_failed.emit(f"Upload failed: {err}"))
        self._upload_pool.start(job)
