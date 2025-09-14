import os
import pyperclip
from drivebox.screen_recorder import ScreenRecorder
from drivebox.upload import upload_file_to_drivebox

class RecordingService:
    def __init__(self, notifier, upload_func, app_state):
        self.recorder = ScreenRecorder()
        self.notifier = notifier
        self.upload_func = upload_func
        self.app_state = app_state
        self.is_recording = False

    def _do_start(self):
        """Worker: runs inside AppState thread."""
        try:
            self.recorder.start_recording()
            self.is_recording = True
            print("Screen recording started.")
            self.notifier.notify("Screen Recording", "Recording started")
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.notifier.notify("Screen Recording Failed", str(e))
            self.is_recording = False
            raise

    def _do_stop_and_upload(self):
        """Worker: runs inside AppState thread."""
        try:
            output_file = self.recorder.stop_recording()
            self.is_recording = False
            if output_file and os.path.exists(output_file):
                link = self.upload_func(output_file)
                pyperclip.copy(link)
                print(f"Recording uploaded! Link copied to clipboard: {link}")
                self.notifier.notify("Recording Uploaded", "Link copied to clipboard")
                return link
            else:
                raise RuntimeError("No recording file found.")
        except Exception as e:
            print(f"Recording upload failed: {e}")
            self.notifier.notify("Recording Failed", str(e))
            raise

    def start_recording(self):
        if self.is_recording:
            self.notifier.notify("Screen Recording", "Already recording")
            return
        self.notifier.notify("Queued Task", "Recording start queued")
        self.app_state.enqueue(self._do_start)

    def stop_and_upload(self):
        if not self.is_recording:
            self.notifier.notify("Screen Recording", "Not currently recording")
            return
        self.notifier.notify("Queued Task", "Recording stop+upload queued")
        self.app_state.enqueue(self._do_stop_and_upload)