from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from drivebox.utils import resource_path

def create_tray_menu(app, options_window, screenshot_service, recording_service):
    tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), app)

    menu = QMenu()

    menu_items = [
        ("Take Fullscreen Screenshot", screenshot_service.take_fullscreen),
        ("Take Region Screenshot", lambda: screenshot_service.take_region(lambda: None)),
        None,
        ("Start Screen Recording", recording_service.start_recording),
        ("Stop & Upload Recording", recording_service.stop_and_upload),
        None,
        ("Options", options_window.show),
        None,
        ("Exit", app.quit),
    ]

    action_references = []
    for item in menu_items:
        if item is None:
            menu.addSeparator()
        else:
            text, callback = item
            action = QAction(text)
            action.triggered.connect(callback)
            menu.addAction(action)
            action_references.append(action)

    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("DriveBox")
    tray_icon.show()

    return tray_icon, action_references