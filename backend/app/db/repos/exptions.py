"""
Custom exceptions for database repository operations.

This module defines specific exceptions that can be raised during
database repository interactions to provide more detailed error handling.
"""


class BaseDatabaseException(Exception):
    """Base exception for database errors."""

    pass


class ChatUsernameAlreadyExistsException(BaseDatabaseException):
    """Exception raised when a chat username already exists."""

    pass
