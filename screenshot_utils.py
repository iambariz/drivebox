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
            print(f"Selection result: {result}, Accepted value: {QDialog.Accepted}")
            print(f"Has selected rectangle: {selector.selected_rect is not None}")
            
            if result == QDialog.Accepted and selector.selected_rect:
                filename = os.path.join(self.temp_dir, f"screenshot_{uuid.uuid4()}.png")
                print(f"Attempting to save to: {filename}")
                screen = QApplication.primaryScreen()
                
                pixmap = screen.grabWindow(
                    0,
                    selector.selected_rect.x(),
                    selector.selected_rect.y(),
                    selector.selected_rect.width(),
                    selector.selected_rect.height()
                )
                saved = pixmap.save(filename)
                print(f"Save successful: {saved}")
                return filename
            else:
                print("Selection was cancelled or no region was selected")
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
