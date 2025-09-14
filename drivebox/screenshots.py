import os
import pyperclip
from drivebox.upload import upload_file_to_drivebox
from drivebox.screenshot_utils import Screenshotter

class ScreenshotService:
    def __init__(self, notifier, app_state):
        self.ss = Screenshotter()
        self.notifier = notifier
        self.app_state = app_state

    def _process_and_upload(self, filename, success_title, fail_title):
        """Internal worker: runs inside AppState thread."""
        if filename and os.path.exists(filename):
            try:
                link = upload_file_to_drivebox(filename)
                pyperclip.copy(link)
                if os.path.exists(filename):
                    os.remove(filename)
                print(f"{success_title}! Link copied to clipboard: {link}")
                self.notifier.notify(success_title, "Link copied to clipboard")
                return link
            except Exception as e:
                print(f"Upload failed: {e}")
                self.notifier.notify("Upload Failed", str(e))
                raise
        else:
            print(f"{fail_title}.")
            self.notifier.notify(fail_title, "Could not capture screenshot")
            raise RuntimeError("Screenshot capture failed")

    def take_fullscreen(self):
        # Capture synchronously (fast)
        filename = self.ss.take_fullscreen()
        # Upload asynchronously
        self.app_state.enqueue(self._process_and_upload, filename,
                               "Screenshot Uploaded", "Screenshot Failed")
        self.notifier.notify("Queued Task", "Fullscreen screenshot queued")

    def take_region(self, restart_listener_callback):
        filename = None
        try:
            filename = self.ss.take_region()
            self.app_state.enqueue(self._process_and_upload, filename,
                                   "Region Screenshot Uploaded", "Region Screenshot Failed")
            self.notifier.notify("Queued Task", "Region screenshot queued")
        finally:
            restart_listener_callback()