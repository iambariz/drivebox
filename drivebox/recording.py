import pyperclip
from drivebox.screen_recorder import ScreenRecorder
from drivebox.recording_worker import RecordingStopper

class RecordingService:
    def __init__(self, notifier, upload_func):
        self.recorder = ScreenRecorder()
        self.notifier = notifier
        self.upload_func = upload_func
        self.active_threads = []

    def start_recording(self):
        try:
            self.recorder.start_recording()
            self.notifier.notify("Screen Recording", "Recording started")
            print("Screen recording started.")
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.notifier.notify("Screen Recording Failed", str(e))

    def stop_and_upload(self):
        stopper = RecordingStopper(self.recorder, self.upload_func)
        stopper.finished.connect(self.handle_finished)
        self.active_threads.append(stopper)
        stopper.finished.connect(lambda *_: self.active_threads.remove(stopper))
        stopper.start()

    def handle_finished(self, link, error_message):
        if link:
            pyperclip.copy(link)
            print(f"Recording uploaded! Link copied to clipboard: {link}")
            self.notifier.notify("Recording Uploaded", "Link copied to clipboard")
        else:
            print(f"Recording upload failed: {error_message}")
            self.notifier.notify("Recording Failed", error_message)