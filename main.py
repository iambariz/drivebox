import sys
from threading import Thread
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from screenshot import take_screenshot
from upload import upload_file_to_drivebox
from settings import load_settings
import pyperclip
import os

from ui.options_window import OptionsWindow

hotkey_listener = None

def parse_hotkey(hotkey_str):
    keys = set()
    for part in hotkey_str.lower().split('+'):
        part = part.strip()
        if part == "ctrl":
            keys.add(keyboard.Key.ctrl_l)
        elif part == "alt":
            keys.add(keyboard.Key.alt_l)
        elif part == "shift":
            keys.add(keyboard.Key.shift_l)
        elif len(part) == 1:
            keys.add(keyboard.KeyCode(char=part))
    return keys

def take_and_upload():
    filename = take_screenshot()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Screenshot failed.")

def start_hotkey_listener(hotkey_str):
    global hotkey_listener

    COMBO = parse_hotkey(hotkey_str)
    current = set()

    def on_press(key):
        if key in COMBO:
            current.add(key)
        if all(k in current for k in COMBO):
            on_hotkey()

    def on_release(key):
        if key in current:
            current.remove(key)

    # Stop previous listener if running
    if hotkey_listener is not None:
        hotkey_listener.stop()

    hotkey_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    hotkey_listener.start()
    hotkey_listener.join()  # Keeps the thread alive

def on_hotkey():
    print("Hotkey pressed!")
    take_and_upload()

def update_hotkey(new_hotkey):
    print(f"Updating hotkey to: {new_hotkey}")
    # Always start the listener in a new thread
    global hotkey_listener
    if hotkey_listener is not None:
        hotkey_listener.stop()
    Thread(target=start_hotkey_listener, args=(new_hotkey,), daemon=True).start()

def main():
    # Start hotkey listener in a background thread
    settings = load_settings()
    hotkey = settings.get("hotkey", "Ctrl+Alt+X")
    Thread(target=start_hotkey_listener, args=(hotkey,), daemon=True).start()

    app = QApplication(sys.argv)
    options_window = OptionsWindow(hotkey_callback=update_hotkey)
    tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)
    menu = QMenu()
    options_action = QAction("Options")
    options_action.triggered.connect(options_window.show)
    # screenshot_action = QAction("Take Screenshot")
    # screenshot_action.triggered.connect(take_and_upload)
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(options_action)
    # menu.addAction(screenshot_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
