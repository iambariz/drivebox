from PyQt5.QtCore import QThread, pyqtSignal
import os

class RecordingStopper(QThread):
    finished = pyqtSignal(str, str)  # (link, error_message)

    def __init__(self, recorder, upload_func):
        super().__init__()
        self.recorder = recorder
        self.upload_func = upload_func

    def run(self):
        try:
            output_file = self.recorder.stop_recording()
            if output_file and os.path.exists(output_file):
                link = self.upload_func(output_file)
                os.remove(output_file)
                self.finished.emit(link, "")
            else:
                self.finished.emit("", "No recording file found.")
        except Exception as e:
            self.finished.emit("", str(e))
