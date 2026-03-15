"""Unit tests for SecureFileService."""

import json
import stat

import pytest

from drivebox.storage.file_service import SecureFileService


def test_ensure_directory_creates_dir(tmp_path):
    new_dir = tmp_path / "subdir"
    SecureFileService.ensure_directory(new_dir)
    assert new_dir.is_dir()


def test_ensure_directory_is_idempotent(tmp_path):
    SecureFileService.ensure_directory(tmp_path)  # already exists — should not raise


def test_read_json_returns_dict(tmp_path):
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"key": "value"}))
    result = SecureFileService.read_json(f)
    assert result == {"key": "value"}


def test_read_json_raises_on_missing_file(tmp_path):
    with pytest.raises(ValueError, match="Failed to read"):
        SecureFileService.read_json(tmp_path / "missing.json")


def test_read_json_raises_on_invalid_json(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("not json")
    with pytest.raises(ValueError, match="Failed to read"):
        SecureFileService.read_json(f)


def test_read_json_raises_on_non_dict(tmp_path):
    f = tmp_path / "list.json"
    f.write_text(json.dumps([1, 2, 3]))
    with pytest.raises(TypeError, match="Expected dict"):
        SecureFileService.read_json(f)


def test_write_and_read_pickle(tmp_path):
    f = tmp_path / "data.pkl"
    data = {"token": "abc123"}
    SecureFileService.write_pickle(f, data)
    result = SecureFileService.read_pickle(f)
    assert result == data


def test_write_pickle_sets_permissions(tmp_path):
    f = tmp_path / "data.pkl"
    SecureFileService.write_pickle(f, {})
    mode = stat.S_IMODE(f.stat().st_mode)
    assert mode == 0o600


def test_read_pickle_raises_on_missing_file(tmp_path):
    with pytest.raises(ValueError, match="Failed to read pickle"):
        SecureFileService.read_pickle(tmp_path / "missing.pkl")


def test_delete_file_returns_true_when_exists(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("data")
    assert SecureFileService.delete_file(f) is True
    assert not f.exists()


def test_delete_file_returns_false_when_missing(tmp_path):
    assert SecureFileService.delete_file(tmp_path / "missing.txt") is False
