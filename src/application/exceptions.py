class ApplicationException(Exception):
    """Base exception for application layer errors."""
    pass

class InvalidCommandException(ApplicationException):
    """Raised when an invalid command is executed."""
    pass
