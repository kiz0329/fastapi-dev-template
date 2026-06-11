from fastapi import HTTPException, status
from ....system.error import (
    CRUDErrorBase,
    ResourceNotFoundError,
    UniqueConstraintError,
    CheckConstraintError,
    ExclusionConstraintError,
    ForeignKeyConstraintError,
    NotNullConstraintError,
)

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
