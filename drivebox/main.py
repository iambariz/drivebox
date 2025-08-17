import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

from drivebox.settings import load_settings
from drivebox.ui.options_window import OptionsWindow
from drivebox.hotkeys import HotkeyManager
from drivebox.notification import Notifier
from drivebox.screenshot import ScreenshotService
from drivebox.recording import RecordingService
from drivebox.tray import create_tray_menu
from drivebox.upload import upload_file_to_drivebox

# Signal bridge for thread-safe hotkey communication
class HotkeyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    bridge = HotkeyBridge()
    notifier = Notifier()
    screenshot_service = ScreenshotService(notifier)
    recording_service = RecordingService(notifier, upload_file_to_drivebox)

    # Hotkey setup
    hotkey_manager = HotkeyManager(bridge)
    settings = load_settings()
    hotkey_manager.register_hotkey(settings.get("hotkey", "Ctrl+Alt+X"), "fullscreen", "fullscreen")
    hotkey_manager.register_hotkey(settings.get("hotkey_region", "Ctrl+Alt+R"), "region", "region")
    hotkey_manager.register_hotkey(settings.get("hotkey_record_start", "Ctrl+Alt+S"), "record_start", "record_start")
    hotkey_manager.register_hotkey(settings.get("hotkey_record_stop", "Ctrl+Alt+E"), "record_stop", "record_stop")

    # Connect hotkeys to actions
    bridge.hotkey_activated.connect(lambda hotkey_name: {
        "fullscreen": screenshot_service.take_fullscreen,
        "region": lambda: screenshot_service.take_region(hotkey_manager.start_listener),
        "record_start": recording_service.start_recording,
        "record_stop": recording_service.stop_and_upload,
    }.get(hotkey_name, lambda: None)())

    # Options window
    options_window = OptionsWindow(
        hotkey_callback=lambda new_hotkey: hotkey_manager.register_hotkey(
            new_hotkey, "fullscreen", "fullscreen"
        )
    )

    # Tray menu
    tray_icon, action_references = create_tray_menu(
        app, options_window, screenshot_service, recording_service
    )

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()