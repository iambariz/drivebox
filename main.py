import sys
from threading import Thread
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from upload import upload_file_to_drivebox
from settings import load_settings
from utils import resource_path
import pyperclip
import os
from screenshot_utils import Screenshotter
from ui.options_window import OptionsWindow

# Dictionary to track multiple hotkey listeners
hotkey_listeners = {}
ss = Screenshotter()

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
    filename = ss.take_fullscreen()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Screenshot failed.")

def take_region_and_upload():
    filename = ss.take_region()
    if filename and os.path.exists(filename):
        link = upload_file_to_drivebox(filename)
        pyperclip.copy(link)
        os.remove(filename)
        print(f"Region screenshot uploaded! Link copied to clipboard: {link}")
    else:
        print("Region screenshot failed.")

def start_hotkey_listener(hotkey_str, action_callback, listener_name):
    global hotkey_listeners
    
    # Stop previous listener with this name if exists
    stop_listener(listener_name)
    
    COMBO = parse_hotkey(hotkey_str)
    current = set()

    def on_press(key):
        if key in COMBO:
            current.add(key)
        if all(k in current for k in COMBO):
            action_callback()

    def on_release(key):
        if key in current:
            current.remove(key)

    # Create and start new listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    hotkey_listeners[listener_name] = listener
    listener.daemon = True
    listener.start()
    print(f"Started listener '{listener_name}' for hotkey: {hotkey_str}")

def stop_listener(listener_name):
    global hotkey_listeners
    if listener_name in hotkey_listeners:
        hotkey_listeners[listener_name].stop()
        del hotkey_listeners[listener_name]
        print(f"Stopped listener: {listener_name}")

def update_hotkey(new_hotkey, action_callback=None, listener_name="default"):
    print(f"Updating hotkey '{listener_name}' to: {new_hotkey}")
    # If no specific action provided, use default
    if action_callback is None:
        action_callback = take_and_upload
    
    # Start in the main thread to avoid blocking with Thread.join()
    start_hotkey_listener(new_hotkey, action_callback, listener_name)

def main():
    # Load settings
    settings = load_settings()
    
    # Start hotkey listeners
    fullscreen_hotkey = settings.get("hotkey", "Ctrl+Alt+X")
    region_hotkey = settings.get("hotkey_region", "Ctrl+Alt+R")
    
    # Start each listener with its own name and action
    update_hotkey(fullscreen_hotkey, take_and_upload, "fullscreen")
    update_hotkey(region_hotkey, take_region_and_upload, "region")

    app = QApplication(sys.argv)
    options_window = OptionsWindow(hotkey_callback=lambda new_hotkey: update_hotkey(new_hotkey, take_and_upload, "fullscreen"))
    tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), app)

    menu = QMenu()
    options_action = QAction("Options")
    options_action.triggered.connect(options_window.show)

    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)

    menu.addAction(options_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()