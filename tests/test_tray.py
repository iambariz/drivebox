import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtCore import Qt
from drivebox.tray import create_tray_menu


@pytest.mark.usefixtures("qtbot")
def test_create_tray_menu_with_clicks(qtbot):
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
    assert len(actions) == 6  # 9 items in menu, 3 are None → 6 actions

    # ✅ Simulate user clicks
    qtbot.mouseClick(actions[0].parentWidget(), Qt.LeftButton)
    screenshot_service.take_fullscreen.assert_called_once()

    qtbot.mouseClick(actions[1].parentWidget(), Qt.LeftButton)
    screenshot_service.take_region.assert_called_once()

    qtbot.mouseClick(actions[2].parentWidget(), Qt.LeftButton)
    recording_service.start_recording.assert_called_once()

    qtbot.mouseClick(actions[3].parentWidget(), Qt.LeftButton)
    recording_service.stop_and_upload.assert_called_once()

    qtbot.mouseClick(actions[4].parentWidget(), Qt.LeftButton)
    options_window.show.assert_called_once()

    # ✅ Exit action should call app.quit
    with patch.object(app, "quit") as mock_quit:
        qtbot.mouseClick(actions[5].parentWidget(), Qt.LeftButton)
        mock_quit.assert_called_once()