from fastapi import status

# This module defines custom exceptions for CRUD operations in the application.


class CRUDErrorBase(Exception):
    """Base class for CRUD-related exceptions."""

    def __init__(self, http_status: int, message: str):
        self.http_status = http_status
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(CRUDErrorBase):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class UniqueConstraintError(CRUDErrorBase):
    """Exception raised when a unique constraint is violated."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_409_CONFLICT, message)


class ForeignKeyConstraintError(CRUDErrorBase):
    """Exception raised when a foreign key constraint is violated."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class NotNullConstraintError(CRUDErrorBase):
    """Exception raised when a not-null constraint is violated."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class CheckConstraintError(CRUDErrorBase):
    """Exception raised when a check constraint is violated."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class ExclusionConstraintError(CRUDErrorBase):
    """Exception raised when an exclusion constraint is violated."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)
