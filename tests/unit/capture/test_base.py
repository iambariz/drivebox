"""Unit tests for capture.base utilities."""

import re

from drivebox.capture import generate_filename, save_local


def test_generate_filename_format():
    filename = generate_filename()
    assert re.match(r"screenshot_\d{8}_\d{6}\.png", filename)


def test_generate_filename_is_unique():
    names = {generate_filename() for _ in range(3)}
    assert all(name.startswith("screenshot_") for name in names)


def test_save_local_writes_bytes(tmp_path):
    path = tmp_path / "shot.png"
    save_local(b"data", path)
    assert path.read_bytes() == b"data"
