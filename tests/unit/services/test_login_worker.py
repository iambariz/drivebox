"""Unit tests for LoginJob."""

from unittest.mock import MagicMock

import pytest
from google_auth_oauthlib.flow import WSGITimeoutError
from PyQt5.QtCore import QCoreApplication

from drivebox.services import LoginJob


_app = QCoreApplication.instance() or QCoreApplication([])


def run_job(auth_service):
    job = LoginJob(auth_service)
    succeeded = []
    failed = []
    job.signals.succeeded.connect(lambda: succeeded.append(True))
    job.signals.failed.connect(failed.append)
    job.run()
    return succeeded, failed


def test_run_emits_succeeded():
    auth_service = MagicMock()

    succeeded, failed = run_job(auth_service)

    auth_service.get_credentials.assert_called_once()
    assert succeeded == [True]
    assert failed == []


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (FileNotFoundError("No client secrets"), "Could not find Google OAuth credentials"),
        (WSGITimeoutError("timed out"), "Sign-in timed out"),
        (RuntimeError("boom"), "Authentication failed"),
    ],
)
def test_run_emits_failed_with_message(error, expected):
    auth_service = MagicMock()
    auth_service.get_credentials.side_effect = error

    succeeded, failed = run_job(auth_service)

    assert succeeded == []
    assert len(failed) == 1
    assert expected in failed[0]
