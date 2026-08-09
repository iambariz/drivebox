import logging

from drivebox.capture import Capturer, generate_filename
from drivebox.clipboard import ClipboardManager
from drivebox.drive import DriveClient


logger = logging.getLogger(__name__)


class ScreenshotService:
    def __init__(
        self,
        capture: Capturer,
        drive_client: DriveClient,
        clipboard: ClipboardManager,
    ) -> None:
        self.capture = capture
        self.drive_client = drive_client
        self.clipboard = clipboard

    def take_and_upload_screenshot(self) -> str:
        """Take screenshot, upload to Drive, copy link to clipboard."""
        logger.info("Taking screenshot...")

        # Capture
        image_data = self.capture.capture_fullscreen()
        filename = generate_filename()

        logger.info(f"Uploading {filename}...")

        # Upload and get link
        link = self.drive_client.upload_and_share(image_data, filename)

        # Copy to clipboard
        self.clipboard.copy(link)

        logger.info(f"Done! Link: {link}")
        return link
