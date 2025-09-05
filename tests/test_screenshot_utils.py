import os
import re
from unittest.mock import patch, MagicMock
from drivebox.screenshot_utils import Screenshotter


def test_get_formatted_filename(tmp_path, monkeypatch):
    monkeypatch.setattr("drivebox.screenshot_utils.tempfile.gettempdir", lambda: str(tmp_path))
    ss = Screenshotter()
    filename = ss._get_formatted_filename("test_")
    assert filename.startswith(str(tmp_path))
    assert filename.endswith("_screenshot.png")
    assert re.search(r"test_\d{4}-\d{2}-\d{2}", filename)


def test_select_region_accept(monkeypatch):
    class FakeRect:
        def left(self): return 10
        def top(self): return 20
        def width(self): return 100
        def height(self): return 200

    class FakeSelector:
        Accepted = 1
        def exec_(self): return self.Accepted
        @property
        def selected_rect(self): return FakeRect()

    monkeypatch.setattr("drivebox.screenshot_utils.RegionSelector", lambda: FakeSelector())
    ss = Screenshotter()
    region = ss.select_region()
    assert region == (10, 20, 100, 200)


def test_select_region_reject(monkeypatch):
    class FakeSelector:
        Accepted = 1
        def exec_(self): return 0  # Rejected
        @property
        def selected_rect(self): return None

    monkeypatch.setattr("drivebox.screenshot_utils.RegionSelector", lambda: FakeSelector())
    ss = Screenshotter()
    region = ss.select_region()
    assert region is None


def test_take_fullscreen(monkeypatch, tmp_path):
    fake_img = MagicMock()
    fake_img.rgb = b"rgb"
    fake_img.size = (100, 100)

    fake_sct = MagicMock()
    fake_sct.monitors = [None, {"left": 0, "top": 0, "width": 100, "height": 100}]
    fake_sct.grab.return_value = fake_img

    monkeypatch.setattr("drivebox.screenshot_utils.tempfile.gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr("mss.mss", lambda: fake_sct)
    monkeypatch.setattr("mss.tools.to_png", lambda rgb, size, output: open(output, "w").write("fake"))

    ss = Screenshotter()
    filename = ss.take_fullscreen()
    assert os.path.exists(filename)
    with open(filename) as f:
        assert f.read() == "fake"


def test_take_region_success(monkeypatch, tmp_path):
    fake_img = MagicMock()
    fake_img.rgb = b"rgb"
    fake_img.size = (50, 50)

    fake_sct = MagicMock()
    fake_sct.grab.return_value = fake_img

    class FakeSelector:
        Accepted = 1
        def exec_(self): return self.Accepted
        @property
        def selected_rect(self):
            class Rect:
                def left(self): return 0
                def top(self): return 0
                def width(self): return 50
                def height(self): return 50
            return Rect()

    monkeypatch.setattr("drivebox.screenshot_utils.RegionSelector", lambda: FakeSelector())
    monkeypatch.setattr("drivebox.screenshot_utils.tempfile.gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr("mss.mss", lambda: fake_sct)
    monkeypatch.setattr("mss.tools.to_png", lambda rgb, size, output: open(output, "w").write("region"))

    ss = Screenshotter()
    filename = ss.take_region()
    assert os.path.exists(filename)
    with open(filename) as f:
        assert f.read() == "region"


def test_take_region_no_selection(monkeypatch):
    class FakeSelector:
        Accepted = 1
        def exec_(self): return 0
        @property
        def selected_rect(self): return None

    monkeypatch.setattr("drivebox.screenshot_utils.RegionSelector", lambda: FakeSelector())
    ss = Screenshotter()
    result = ss.take_region()
    assert result is None