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
from notifypy import Notify

# Create a signal bridge to safely communicate between threads
class HotkeyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

# Global instances
keyboard_listener = None
ss = Screenshotter()
registered_hotkeys = {}
app = None
bridge = HotkeyBridge()
options_window = None  # Make options_window global to prevent garbage collection

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

# Add a helper function for showing notifications
def show_notification(title, message, icon_path=None):
    """Show a desktop notification with the specified title and message"""
    notification = Notify()
    notification.title = title
    notification.message = message
    
    # Use the app icon if none provided
    if icon_path is None:
        icon_path = resource_path("icon.png")
    
    notification.icon = icon_path
    notification.send()

def take_and_upload():
    filename = ss.take_fullscreen()
    if filename and os.path.exists(filename):
        try:
            link = upload_file_to_drivebox(filename)
            pyperclip.copy(link)
            os.remove(filename)
            print(f"Screenshot uploaded! Link copied to clipboard: {link}")
            show_notification("Screenshot Uploaded", "Link copied to clipboard")
        except Exception as e:
            print(f"Upload failed: {e}")
            show_notification("Upload Failed", str(e))
    else:
        print("Screenshot failed.")
        show_notification("Screenshot Failed", "Could not capture screenshot")

def take_region_and_upload():
    global keyboard_listener
    # Stop the listener temporarily
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None

    try:
        filename = ss.take_region()
        if filename and os.path.exists(filename):
            try:
                link = upload_file_to_drivebox(filename)
                pyperclip.copy(link)
                os.remove(filename)
                print(f"Region screenshot uploaded! Link copied to clipboard: {link}")
                show_notification("Region Screenshot Uploaded", "Link copied to clipboard")
            except Exception as e:
                print(f"Upload failed: {e}")
                show_notification("Upload Failed", str(e))
        else:
            print("Region screenshot failed.")
            show_notification("Screenshot Failed", "Could not capture region screenshot")
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
    global app, options_window, action_references
    
    # Create QApplication first
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Set up signal connections
    setup_hotkey_connections()

    # Load settings
    settings = load_settings()

    register_hotkey(settings.get("hotkey", "Ctrl+Alt+X"), "fullscreen", "fullscreen")
    register_hotkey(settings.get("hotkey_region", "Ctrl+Alt+R"), "region", "region")

    # Create system tray icon
    tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), app)

    menu = QMenu()
    options_window = OptionsWindow(hotkey_callback=lambda new_hotkey: update_hotkey(new_hotkey, "fullscreen", "fullscreen"))

    # Define menu items
    menu_items = [
        ("Take Fullscreen Screenshot", take_and_upload),
        ("Take Region Screenshot", take_region_and_upload),
        None,  # separator
        ("Options", options_window.show),
        None,  # separator
        ("Exit", app.quit)
    ]

    # Store references to all created actions to prevent garbage collection
    action_references = []

    # Create menu items
    for item in menu_items:
        if item is None:
            menu.addSeparator()
        else:
            text, callback = item
            action = QAction(text)
            action.triggered.connect(callback)
            menu.addAction(action)
            # Keep a reference to the action
            action_references.append(action)

    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()

    # Clean up on exit
    app.aboutToQuit.connect(lambda: keyboard_listener.stop() if keyboard_listener else None)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()