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
    """Check that the frozen build bundled all modules and data files (used by CI)."""
    # Offline, uses the bundled discovery document
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
