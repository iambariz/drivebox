# screenshot.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QDialog
import os
import sys
import uuid
import tempfile
from region_selector import RegionSelector

class Screenshotter:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.temp_dir = tempfile.gettempdir()

    def select_region(self):
        selector = RegionSelector()
        if selector.exec_() == selector.Accepted and selector.selected_rect:
            rect = selector.selected_rect
            return rect.left(), rect.top(), rect.width(), rect.height()
        return None

    def take_fullscreen(self, filename='screenshot.png'):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save(filename, 'png')
        print(f"Screenshot saved as {filename}")
        return filename

    def take_region(self):
        """Take a screenshot of a selected region"""
        try:
            selector = RegionSelector()
            selector.showFullScreen()
            
            result = selector.exec_()
            if result == QDialog.Accepted and selector.selected_rect:
                filename = os.path.join(self.temp_dir, f"screenshot_{uuid.uuid4()}.png")
                screen = QApplication.primaryScreen()
                
                pixmap = screen.grabWindow(
                    0,
                    selector.selected_rect.x(),
                    selector.selected_rect.y(),
                    selector.selected_rect.width(),
                    selector.selected_rect.height()
                )
                pixmap.save(filename)
                return filename
        except Exception as e:
            print(f"Error taking region screenshot: {e}")
        return None

    def take_all_screens(self):
        for i, screen in enumerate(QGuiApplication.screens()):
            screenshot = screen.grabWindow(0)
            filename = f"screenshot_screen_{i+1}.png"
            screenshot.save(filename, 'png')
            print(f"Screenshot saved as {filename}")

if __name__ == "__main__":
    ss = Screenshotter()
    ss.take_fullscreen()
    ss.take_region()
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
#     if system == "Windows":import tempfile
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