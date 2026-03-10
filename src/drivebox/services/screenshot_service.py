import logging

from drivebox.auth import get_gdrive_service
from drivebox.capture import ScreenCapture
from drivebox.clipboard import ClipboardManager
from drivebox.drive import DriveClient


logger = logging.getLogger(__name__)


class ScreenshotService:
    def __init__(self) -> None:
        self.drive_service = get_gdrive_service()
        self.drive_client = DriveClient(self.drive_service)
        self.capture = ScreenCapture()
        self.clipboard = ClipboardManager()

    def take_and_upload_screenshot(self) -> str:
        """Take screenshot, upload to Drive, copy link to clipboard."""
        logger.info("Taking screenshot...")

        # Capture
        image_data = self.capture.capture_fullscreen()
        filename = self.capture.generate_filename()

        logger.info(f"Uploading {filename}...")

        # Upload and get link
        link = self.drive_client.upload_and_share(image_data, filename)

        # Copy to clipboard
        self.clipboard.copy(link)

        logger.info(f"Done! Link: {link}")
        return link
