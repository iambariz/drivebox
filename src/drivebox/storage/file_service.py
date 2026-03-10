import json
import pickle
from pathlib import Path
from typing import Any


class SecureFileService:
    @staticmethod
    def ensure_directory(path: Path, mode: int = 0o700) -> None:
        path.mkdir(mode=mode, exist_ok=True)

    @staticmethod
    def read_json(path: Path) -> dict[str, Any]:
        try:
            with path.open() as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to read {path}: {e}") from e
        else:
            if not isinstance(data, dict):
                raise TypeError(f"Expected dict, got {type(data)}")
            return data

    @staticmethod
    def read_pickle(path: Path) -> Any:
        try:
            with path.open("rb") as f:
                return pickle.load(f)
        except (OSError, pickle.UnpicklingError) as e:
            raise ValueError(f"Failed to read pickle {path}: {e}") from e

    @staticmethod
    def write_pickle(path: Path, data: Any, mode: int = 0o600) -> None:
        try:
            with path.open("wb") as f:
                pickle.dump(data, f)
            path.chmod(mode)
        except OSError as e:
            raise OSError(f"Failed to write {path}: {e}") from e

    @staticmethod
    def delete_file(path: Path) -> bool:
        if path.exists():
            path.unlink()
            return True
        return False
