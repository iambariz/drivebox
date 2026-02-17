import logging

import pyperclip


logger = logging.getLogger(__name__)


class ClipboardManager:
    @staticmethod
    def copy(text: str) -> None:
        """Copy text to clipboard."""
        pyperclip.copy(text)
        logger.info(f"Copied to clipboard: {text}")

    @staticmethod
    def paste() -> str:
        """Get text from clipboard."""
        content: str = str(pyperclip.paste())
        return content
