class AuthenticationError(Exception):
    """Base exception for authentication errors."""


class CredentialsNotFoundError(AuthenticationError):
    """Raised when credentials cannot be located."""


class TokenRefreshError(AuthenticationError):
    """Raised when token refresh fails."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid or malformed."""
