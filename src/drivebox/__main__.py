"""Main entry point for Drivebox application."""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv


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


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Drivebox starting...")

    from drivebox.app import main as app_main

    return app_main()


if __name__ == "__main__":
    sys.exit(main())
