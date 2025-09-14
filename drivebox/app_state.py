import queue
from PyQt5.QtCore import QThread, pyqtSignal

class TaskWorker(QThread):
    task_done = pyqtSignal(str, str)  # result, error

    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                func, args, kwargs = self.task_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                result = func(*args, **kwargs)
                self.task_done.emit(str(result) if result else "", "")
            except Exception as e:
                self.task_done.emit("", str(e))
            finally:
                self.task_queue.task_done()

    def stop(self):
        self.running = False


class AppState:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.worker = TaskWorker(self.task_queue)
        self.worker.start()

    def enqueue(self, func, *args, **kwargs):
        """Add a task to the queue."""
        self.task_queue.put((func, args, kwargs))