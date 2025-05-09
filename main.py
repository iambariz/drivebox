import sys
import threading
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from screenshot import take_screenshot
from auth import get_gdrive_service
from upload import upload_file_to_drivebox
import pyperclip
import os

def login_to_gdrive():
    service = get_gdrive_service()
    if service:
        print("Google Drive authentication successful.")
        # Optional: Show a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Google Drive authentication successful!")
        msg.setWindowTitle("DriveBox")
        msg.exec_()
    else:
        print("Google Drive authentication failed.")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Google Drive authentication failed!")
        msg.setWindowTitle("DriveBox")
        msg.exec_()

def take_and_upload():
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Screenshot failed.")


def on_hotkey():
    print("Hotkey pressed!")
    take_and_upload()

def start_hotkey_listener():
    # Todo: Change hotkey / Give user option to change hotkey
    COMBO = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char='x')}
    current = set()

    def on_press(key):
        if key in COMBO:
            current.add(key)
        if all(k in current for k in COMBO):
            on_hotkey()

    def on_release(key):
        if key in current:
            current.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main():
    # Start hotkey listener in a separate thread
    hotkey_thread = threading.Thread(target=start_hotkey_listener, daemon=True)
    hotkey_thread.start()

    app = QApplication(sys.argv)
    tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)
    menu = QMenu()
    login_action = QAction("Login to Google Drive")
    login_action.triggered.connect(login_to_gdrive)
    screenshot_action = QAction("Take Screenshot")
    screenshot_action.triggered.connect(take_and_upload)
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(login_action)
    menu.addAction(screenshot_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
