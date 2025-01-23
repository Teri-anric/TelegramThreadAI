class BaseDatabaseException(Exception):
    """Base exception for database errors."""
    pass

class ChatUsernameAlreadyExistsException(BaseDatabaseException):
    """Exception raised when a chat username already exists."""
    pass
