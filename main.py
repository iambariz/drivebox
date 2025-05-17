import sys
from threading import Thread
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from upload import upload_file_to_drivebox
from settings import load_settings
from utils import resource_path
import pyperclip
import os
from screenshot_utils import Screenshotter
from ui.options_window import OptionsWindow

# Create a signal bridge to safely communicate between threads
class HotkeyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

# Global instances
keyboard_listener = None
ss = Screenshotter()
registered_hotkeys = {}
app = None
bridge = HotkeyBridge()

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
    return frozenset(keys)

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
    global keyboard_listener
    # Stop the listener temporarily
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None
    
    try:
        filename = ss.take_region()
        if filename and os.path.exists(filename):
            link = upload_file_to_drivebox(filename)
            pyperclip.copy(link)
            os.remove(filename)
            print(f"Region screenshot uploaded! Link copied to clipboard: {link}")
        else:
            print("Region screenshot failed.")
    finally:
        # Restart the keyboard listener
        start_keyboard_listener()

# Connect the hotkey signals to their respective functions
def setup_hotkey_connections():
    bridge.hotkey_activated.connect(lambda hotkey_name: {
        'fullscreen': take_and_upload,
        'region': take_region_and_upload
    }.get(hotkey_name, lambda: None)())

def start_keyboard_listener():
    global keyboard_listener, registered_hotkeys
    
    if not registered_hotkeys:
        return
    
    if keyboard_listener:
        try:
            keyboard_listener.stop()
        except:
            pass
    
    current_keys = set()
    
    def on_press(key):
        current_keys.add(key)
        
        # Check each hotkey combination
        for keys_combo, (callback_name, _) in registered_hotkeys.items():
            if all(k in current_keys for k in keys_combo):
                # Emit signal that will be safely received in the main thread
                bridge.hotkey_activated.emit(callback_name)
    
    def on_release(key):
        if key in current_keys:
            current_keys.remove(key)
    
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.daemon = True
    keyboard_listener.start()
    print(f"Started global keyboard listener with {len(registered_hotkeys)} registered hotkeys")

def register_hotkey(hotkey_str, callback_name, hotkey_name):
    global registered_hotkeys
    
    keys = parse_hotkey(hotkey_str)
    registered_hotkeys[keys] = (callback_name, hotkey_name)
    print(f"Registered hotkey '{hotkey_name}': {hotkey_str}")
    
    start_keyboard_listener()

def update_hotkey(new_hotkey, callback_name="fullscreen", hotkey_name="default"):
    register_hotkey(new_hotkey, callback_name, hotkey_name)

def main():
    global app
    
    # Create QApplication first
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Set up signal connections
    setup_hotkey_connections()
    
    # Load settings
    settings = load_settings()
    
    # Register hotkeys
    fullscreen_hotkey = settings.get("hotkey", "Ctrl+Alt+X")
    region_hotkey = settings.get("hotkey_region", "Ctrl+Alt+R")
    
    register_hotkey(fullscreen_hotkey, "fullscreen", "fullscreen")
    register_hotkey(region_hotkey, "region", "region")

    options_window = OptionsWindow(hotkey_callback=lambda new_hotkey: update_hotkey(new_hotkey, "fullscreen", "fullscreen"))
    tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), app)

    # Create menu
    menu = QMenu()
    
    fullscreen_action = QAction("Take Fullscreen Screenshot")
    fullscreen_action.triggered.connect(take_and_upload)
    
    region_action = QAction("Take Region Screenshot")
    region_action.triggered.connect(take_region_and_upload)
    
    options_action = QAction("Options")
    options_action.triggered.connect(options_window.show)

    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)

    menu.addAction(fullscreen_action)
    menu.addAction(region_action)
    menu.addSeparator()
    menu.addAction(options_action)
    menu.addSeparator()
    menu.addAction(exit_action)
    
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()
    
    # Clean up on exit
    app.aboutToQuit.connect(lambda: keyboard_listener.stop() if keyboard_listener else None)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
