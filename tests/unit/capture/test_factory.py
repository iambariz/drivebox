"""Unit tests for the Capturer factory."""

from unittest.mock import patch

from drivebox.capture import QScreenCapturer, WaylandPortalCapturer, get_capturer


@patch("drivebox.capture.factory.is_wayland", return_value=True)
def test_get_capturer_returns_portal_on_wayland(mock_is_wayland):
    assert isinstance(get_capturer(), WaylandPortalCapturer)


@patch("drivebox.capture.factory.is_wayland", return_value=False)
def test_get_capturer_returns_qscreen_otherwise(mock_is_wayland):
    assert isinstance(get_capturer(), QScreenCapturer)
