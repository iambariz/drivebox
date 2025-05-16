# screenshot.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
import sys
from region_selector import RegionSelector

class Screenshotter:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)

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
    ss.take_fullscreen()
    ss.take_region()
    # ss.take_all_screens()
