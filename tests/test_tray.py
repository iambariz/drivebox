import pytest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication, QAction
from drivebox.tray import create_tray_menu


@pytest.mark.usefixtures("qtbot")
def test_create_tray_menu(qtbot):
    app = QApplication.instance() or QApplication([])

    # Mock services
    screenshot_service = MagicMock()
    recording_service = MagicMock()
    options_window = MagicMock()

    tray_icon, actions = create_tray_menu(
        app, options_window, screenshot_service, recording_service
    )

    # ✅ Tray icon should be a QSystemTrayIcon
    from PyQt5.QtWidgets import QSystemTrayIcon
    assert isinstance(tray_icon, QSystemTrayIcon)

    # ✅ Actions should be a list of QAction
    assert all(isinstance(a, QAction) for a in actions)

    # ✅ Check that the right number of actions were created
    # (menu_items had 9 entries, 3 were None → 6 actions)
    assert len(actions) == 6

    # ✅ Trigger each action and check the right callback is called
    # Fullscreen screenshot
    actions[0].trigger()
    screenshot_service.take_fullscreen.assert_called_once()

    # Region screenshot
    actions[1].trigger()
    screenshot_service.take_region.assert_called_once()

    # Start recording
    actions[2].trigger()
    recording_service.start_recording.assert_called_once()

    # Stop recording
    actions[3].trigger()
    recording_service.stop_and_upload.assert_called_once()

    # Options
    actions[4].trigger()
    options_window.show.assert_called_once()

    # Exit (last action) → should call app.quit
    with pytest.raises(SystemExit):
        actions[5].trigger()