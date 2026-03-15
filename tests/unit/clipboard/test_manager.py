"""Unit tests for ClipboardManager."""

from unittest.mock import patch

from drivebox.clipboard.manager import ClipboardManager


@patch("drivebox.clipboard.manager.pyperclip.copy")
def test_copy_calls_pyperclip(mock_copy):
    ClipboardManager.copy("https://example.com")
    mock_copy.assert_called_once_with("https://example.com")


@patch("drivebox.clipboard.manager.pyperclip.paste", return_value="https://example.com")
def test_paste_returns_clipboard_content(mock_paste):
    result = ClipboardManager.paste()
    assert result == "https://example.com"
