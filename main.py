import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from screenshot import take_screenshot
from upload import upload_file_to_drivebox
import pyperclip
import os

def take_and_upload():
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Screenshot failed.")

def main():
    app = QApplication(sys.argv)
    # Todo: Create a system tray icon
    tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)
    menu = QMenu()
    screenshot_action = QAction("Take Screenshot")
    screenshot_action.triggered.connect(take_and_upload)
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(screenshot_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
