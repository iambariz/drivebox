import os
import pyperclip
from drivebox.upload import upload_file_to_drivebox
from drivebox.screenshot_utils import Screenshotter

class ScreenshotService:
    def __init__(self, notifier):
        self.ss = Screenshotter()
        self.notifier = notifier

    def process_and_upload(self, filename, success_title, fail_title):
        if filename and os.path.exists(filename):
            try:
                link = upload_file_to_drivebox(filename)
                pyperclip.copy(link)
                os.remove(filename)
                print(f"{success_title}! Link copied to clipboard: {link}")
                self.notifier.notify(success_title, "Link copied to clipboard")
            except Exception as e:
                print(f"Upload failed: {e}")
                self.notifier.notify("Upload Failed", str(e))
        else:
            print(f"{fail_title}.")
            self.notifier.notify(fail_title, "Could not capture screenshot")

    def take_fullscreen(self):
        filename = self.ss.take_fullscreen()
        self.process_and_upload(filename, "Screenshot Uploaded", "Screenshot Failed")

    def take_region(self, restart_listener_callback):
        filename = None
        try:
            filename = self.ss.take_region()
            self.process_and_upload(
                filename, "Region Screenshot Uploaded", "Region Screenshot Failed"
            )
        finally:
            restart_listener_callback()