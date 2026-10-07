"""Main entry point for Drivebox application."""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.discovery import build

from drivebox.app import main as app_main


# Load .env file
load_dotenv()


def setup_logging() -> None:
    log_dir = Path.home() / ".drivebox" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "drivebox.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def smoke_test() -> int:
    """Verify a frozen build is complete: every module imports and bundled data loads.

    Run by CI against the built binary, since PyInstaller succeeds even when a
    dependency is missing from the bundle.
    """
    # Offline build from the bundled discovery document; no network or credentials used.
    build("drive", "v3", developerKey="smoke-test", static_discovery=True)
    print("drivebox smoke test OK")
    return 0


def main() -> int:
    if "--smoke-test" in sys.argv:
        return smoke_test()

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Drivebox starting...")

    return app_main()


if __name__ == "__main__":
    sys.exit(main())
