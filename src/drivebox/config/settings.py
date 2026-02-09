from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppSettings:
    """Application settings and paths."""

    app_dir: Path = Path.home() / ".drivebox"
    token_filename: str = "token.pickle"
    credentials_filename: str = "credentials.json"
    sync_dir: Path = Path.home() / "Drivebox"
    log_dir: Path = Path.home() / ".drivebox" / "logs"

    def __post_init__(self) -> None:
        """Ensure directories exist."""
        self.app_dir.mkdir(exist_ok=True)
        self.sync_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

    @property
    def token_path(self) -> Path:
        return self.app_dir / self.token_filename

    @property
    def credentials_path(self) -> Path:
        return self.app_dir / self.credentials_filename
