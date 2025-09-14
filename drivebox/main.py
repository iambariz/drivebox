import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

from drivebox.ui.options_window import OptionsWindow
from drivebox.hotkeys import HotkeyManager
from drivebox.notifications import Notifier
from drivebox.screenshots import ScreenshotService
from drivebox.recording import RecordingService
from drivebox.tray import create_tray_menu
from drivebox.upload import upload_file_to_drivebox
from drivebox.ui.hotkeys_manager import HotkeysManager
from drivebox.app_state import AppState

# Signal bridge for thread-safe hotkey communication
class HotkeyBridge(QObject):
    hotkey_activated = pyqtSignal(str)

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    bridge = HotkeyBridge()
    notifier = Notifier()
    app_state = AppState()
    screenshot_service = ScreenshotService(notifier, app_state)
    recording_service = RecordingService(notifier, upload_file_to_drivebox, app_state)

    # Central hotkey manager
    hotkey_manager = HotkeyManager(bridge)
    hotkeys_manager = HotkeysManager()

    # Register initial hotkeys from settings or defaults
    for action, hotkey in hotkeys_manager.all().items():
        hotkey_manager.register_hotkey(hotkey, action, action)

    # Connect hotkeys -> services
    bridge.hotkey_activated.connect(
        lambda hotkey_name: {
            "fullscreen": screenshot_service.take_fullscreen,
            "region": lambda: screenshot_service.take_region(
                hotkey_manager.start_listener
            ),
            "record_start": recording_service.start_recording,
            "record_stop": recording_service.stop_and_upload,
        }.get(hotkey_name, lambda: None)()
    )

    # Callback for OptionsWindow hotkey changes
    def hotkey_changed(action, new_hotkey):
        hotkey_manager.register_hotkey(new_hotkey, action, action)

    # Options window
    options_window = OptionsWindow(hotkey_callback=hotkey_changed)

    # Tray menu
    tray_icon, action_references = create_tray_menu(
        app, options_window, screenshot_service, recording_service
    )

    def show_result(result, error):
        if error:
            notifier.notify("Task Failed", error)
        elif result:
            print("Task finished:", result)

    app_state.worker.task_done.connect(show_result)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()