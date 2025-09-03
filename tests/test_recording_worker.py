import os
import pytest
from pathlib import Path
from drivebox.recording_worker import RecordingStopper


def test_run_success(tmp_path, qtbot):
    output_file = tmp_path / "recording.mp4"
    output_file.write_text("dummy")

    class FakeRecorder:
        def stop_recording(self):
            return str(output_file)

    def fake_upload(path):
        return "http://link"

    stopper = RecordingStopper(FakeRecorder(), fake_upload)

    with qtbot.waitSignal(stopper.finished, timeout=1000) as blocker:
        stopper.run()

    link, error = blocker.args
    assert link == "http://link"
    assert error == ""
    assert not output_file.exists()


def test_run_no_file(tmp_path, qtbot):
    class FakeRecorder:
        def stop_recording(self):
            return str(tmp_path / "missing.mp4")

    def fake_upload(path):
        raise AssertionError("Should not be called")

    stopper = RecordingStopper(FakeRecorder(), fake_upload)

    with qtbot.waitSignal(stopper.finished, timeout=1000) as blocker:
        stopper.run()

    link, error = blocker.args
    assert link == ""
    assert error == "No recording file found."


def test_run_exception(qtbot):
    class FakeRecorder:
        def stop_recording(self):
            raise RuntimeError("boom")

    def fake_upload(path):
        raise AssertionError("Should not be called")

    stopper = RecordingStopper(FakeRecorder(), fake_upload)

    with qtbot.waitSignal(stopper.finished, timeout=1000) as blocker:
        stopper.run()

    link, error = blocker.args
    assert link == ""
    assert "boom" in error