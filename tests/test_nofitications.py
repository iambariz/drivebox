from unittest.mock import patch
from drivebox.notifications import Notifier

def test_notifier_sends_notification():
    with patch("notifypy.Notify") as MockNotify:
        mock_instance = MockNotify.return_value
        mock_instance.send.return_value = None

        notifier = Notifier()
        notifier.notify("Hello", "World")

        mock_instance.send.assert_called_once()
        assert mock_instance.title == "Hello"
        assert mock_instance.message == "World"