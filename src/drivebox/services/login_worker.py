import logging

from google_auth_oauthlib.flow import WSGITimeoutError
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

from drivebox.auth import GoogleDriveAuthService


logger = logging.getLogger(__name__)


class LoginJobSignals(QObject):
    succeeded = pyqtSignal()
    failed = pyqtSignal(str)


class LoginJob(QRunnable):
    def __init__(self, auth_service: GoogleDriveAuthService) -> None:
        super().__init__()
        self.auth_service = auth_service
        self.signals = LoginJobSignals()

    def run(self) -> None:
        try:
            self.auth_service.get_credentials()
        except FileNotFoundError as e:
            self.signals.failed.emit(f"Could not find Google OAuth credentials.\n\n{e}")
        except WSGITimeoutError:
            logger.warning("Sign-in timed out")
            self.signals.failed.emit("Sign-in timed out. Please try again.")
        except Exception:
            logger.exception("Login failed")
            self.signals.failed.emit("Authentication failed")
        else:
            self.signals.succeeded.emit()
