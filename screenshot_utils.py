# screenshot.py

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QGuiApplication
import sys

class Screenshotter:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)

    class RegionSelector(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Select Region")
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.setWindowState(Qt.WindowFullScreen)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.start = None
            self.end = None
            self.selected_rect = None

        def mousePressEvent(self, event):
            self.start = event.pos()
            self.end = self.start
            self.update()

        def mouseMoveEvent(self, event):
            self.end = event.pos()
            self.update()

        def mouseReleaseEvent(self, event):
            self.end = event.pos()
            self.selected_rect = QRect(self.start, self.end).normalized()
            self.close()

        def paintEvent(self, event):
            if self.start and self.end:
                painter = QPainter(self)
                painter.setPen(QColor(0, 180, 255, 200))
                painter.setBrush(QColor(0, 180, 255, 50))
                rect = QRect(self.start, self.end)
                painter.drawRect(rect.normalized())

    def select_region(self):
        selector = self.RegionSelector()
        selector.show()
        self.app.exec_()
        if selector.selected_rect:
            rect = selector.selected_rect
            return rect.left(), rect.top(), rect.width(), rect.height()
        return None

    def take_fullscreen(self, filename='screenshot.png'):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save(filename, 'png')
        print(f"Screenshot saved as {filename}")
        return filename

    def take_region(self, filename='region.png'):
        region = self.select_region()
        if region:
            screen = QGuiApplication.primaryScreen()
            screenshot = screen.grabWindow(0, region[0], region[1], region[2], region[3])
            screenshot.save(filename, 'png')
            print(f"Region screenshot saved as {filename}")
            return filename
        else:
            print("No region selected.")
            return None

    def take_all_screens(self):
        for i, screen in enumerate(QGuiApplication.screens()):
            screenshot = screen.grabWindow(0)
            filename = f"screenshot_screen_{i+1}.png"
            screenshot.save(filename, 'png')
            print(f"Screenshot saved as {filename}")

if __name__ == "__main__":
    ss = Screenshotter()
    # Full screen screenshot
    ss.take_fullscreen()
    # Region screenshot
    ss.take_region()
    # All screens (uncomment to use)
    # ss.take_all_screens()



# import platform
# import os
# import shutil
# import subprocess

# def is_wayland():
#     """Check if running on Wayland"""
#     return os.environ.get('XDG_SESSION_TYPE') == 'wayland'

# def take_screenshot(filename='screenshot.png'):
#     system = platform.system()

#     # On Linux, check for Wayland first and use appropriate tools
#     if system == "Linux" and is_wayland():
#         print("Detected Wayland session, using native tools...")

#         # Try wl-screenshot (a Wayland-native screenshot tool)
#         if shutil.which("grim"):
#             os.system(f"grim {filename}")
#             print(f"Screenshot saved as {filename} (via grim)")
#             return filename
#         # Try gnome-screenshot (works on GNOME/Wayland via portal)
#         elif shutil.which("gnome-screenshot"):
#             os.system(f"gnome-screenshot -f {filename}")
#             print(f"Screenshot saved as {filename} (via gnome-screenshot)")
#             return filename
#         else:
#             print("No supported Wayland screenshot tool found.")
#             return None

#     # For non-Wayland systems, try mss first
#     try:
#         # Only import mss if we're going to use it
#         import mss
#         import mss.tools

#         print("Taking screenshot using mss...")
#         with mss.mss() as sct:
#             sct.shot(output=filename)
#         print(f"Screenshot saved as {filename} (via mss)")
#         return filename
#     except Exception as e:
#         print(f"mss failed: {e}")

#     # Fallbacks for each OS
#     if system == "Windows":
#         print("Automatic screenshot failed..")
#         # os.system("start snippingtool")
#         return None
#     elif system == "Darwin":  # macOS
#         if shutil.which("screencapture"):
#             os.system(f"screencapture {filename}")
#             print(f"Screenshot saved as {filename} (via screencapture)")
#             return filename
#         else:
#             print("screencapture not found.")
#             return None
#     elif system == "Linux":
#             print("No supported screenshot tool found.")
#             return None
#     else:
#         print("Unsupported OS.")
#         return None

# if __name__ == "__main__":
#     take_screenshot()