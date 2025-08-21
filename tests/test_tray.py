import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QAction
from drivebox.tray import create_tray_menu


@pytest.mark.usefixtures("qtbot")
@pytest.mark.parametrize(
    "index, service_attr",
    [
        (0, "screenshot_service.take_fullscreen"),
        (1, "screenshot_service.take_region"),
        (2, "recording_service.start_recording"),
        (3, "recording_service.stop_and_upload"),
        (4, "options_window.show"),
    ],
)
def test_tray_actions_trigger_callbacks(qtbot, index, service_attr):
    app = QApplication.instance() or QApplication([])

    screenshot_service = MagicMock()
    recording_service = MagicMock()
    options_window = MagicMock()

    tray_icon, actions = create_tray_menu(
        app, options_window, screenshot_service, recording_service
    )

    actions[index].trigger()

    target = eval(service_attr)
    target.assert_called_once()


def test_tray_exit_action_calls_quit(qtbot):
    app = QApplication.instance() or QApplication([])

    screenshot_service = MagicMock()
    recording_service = MagicMock()
    options_window = MagicMock()

    # Patch app.quit BEFORE creating the tray menu
    with patch.object(app, "quit") as mock_quit:
        tray_icon, actions = create_tray_menu(
            app, options_window, screenshot_service, recording_service
        )

        # Trigger Exit action
        actions[5].trigger()
        mock_quit.assert_called_once()