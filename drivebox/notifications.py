class Notifier:
    def __init__(self, default_icon="icon.png"):
        from drivebox.utils import resource_path
        try:
            self.default_icon = resource_path(default_icon)
        except Exception:
            self.default_icon = None

    def notify(self, title, message, icon_path=None):
        from notifypy import Notify
        notification = Notify()
        notification.title = title
        notification.message = message
        try:
            if icon_path or self.default_icon:
                notification.icon = icon_path or self.default_icon
            notification.send()
        except Exception:
            # fallback: try again without setting icon
            try:
                del notification.icon  # clear any bad state
            except Exception:
                pass
            notification.send()