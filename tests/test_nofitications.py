from unittest.mock import patch
from drivebox.notifications import Notifier

def test_notifier_sends_notification():
    notifier = Notifier()

    with patch("notifypy.Notify.send") as mock_send:
        notifier.notify("Test Title", "Test Message")
        mock_send.assert_called_once()