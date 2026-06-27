class PublisherError(Exception):
    """Base exception for recoverable publisher errors."""


class NotFoundError(PublisherError):
    """Raised when a requested record does not exist."""


class InvalidTransitionError(PublisherError):
    """Raised when a draft status transition is not allowed."""


class ValidationError(PublisherError):
    """Raised when input cannot be accepted."""


class AuthConfigError(PublisherError):
    """Raised when LinkedIn OAuth configuration is incomplete."""


class AuthStateError(PublisherError):
    """Raised when OAuth callback state validation fails."""


class LinkedInApiError(PublisherError):
    """Raised when LinkedIn returns an API error."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
