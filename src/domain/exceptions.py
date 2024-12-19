class DomainException(Exception):
    """Base exception for domain-related errors."""
    pass

class EmailNotUniqueException(DomainException):
    """Raised for duplicate email addresses."""
    pass

class CustomerNotFoundException(DomainException):
    """Raised when a customer does not exist."""
    pass

class EmailAlreadyExistsException(DomainException):
    """Raised when a duplicate email is detected in the database."""
    pass
