import os, sys

def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):  # PyInstaller sets this
        base_path = sys._MEIPASS
    else:
        # Base path = this package directory (drivebox/)
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)