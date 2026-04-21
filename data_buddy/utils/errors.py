"""Human-friendly exception types for Data Buddy."""


class BuddyError(Exception):
    """Base exception for user-facing Data Buddy errors."""


class BuddyDataLoadError(BuddyError):
    """Raised when data loading fails with a friendly explanation."""


class BuddyValidationError(BuddyError):
    """Raised when input data is invalid for the requested operation."""
