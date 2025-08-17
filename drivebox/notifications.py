from notifypy import Notify
from drivebox.utils import resource_path

class Notifier:
    def __init__(self, default_icon="resources/icon.png"):
        self.default_icon = resource_path(default_icon)

    def notify(self, title, message, icon_path=None):
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.icon = icon_path or self.default_icon
        notification.send()