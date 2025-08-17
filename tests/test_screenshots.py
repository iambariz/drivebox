import os
from unittest.mock import patch, MagicMock
from drivebox.screenshots import ScreenshotService

def test_take_fullscreen_upload(tmp_path):
    fake_file = tmp_path / "screenshot.png"
    fake_file.write_text("fake image")

    notifier = MagicMock()
    service = ScreenshotService(notifier)

    with patch.object(service.ss, "take_fullscreen", return_value=str(fake_file)), \
         patch("drivebox.screenshots.upload_file_to_drivebox", return_value="http://fake.link"):

        service.take_fullscreen()

    notifier.notify.assert_called_with("Screenshot Uploaded", "Link copied to clipboard")