from typing import   Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from .password import verify_password
from ..model.user import User
from ..database import SessionDep, get_db_session
from ..crud.user import crud as user_crud
from ..system.error import ResourceNotFoundError
from .password import hash_password


DUMMPY_PASSWORD = hash_password("password123")


async def get_user(
        username: str,
        db_session: Annotated[SessionDep, Depends(get_db_session)]
) -> User:
    return await user_crud.get_by_username(username, db_session)


async def authenticate_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: Annotated[SessionDep, Depends(get_db_session)]
) -> User:
    unauthenticated_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = await get_user(form_data.username, db_session)
    except ResourceNotFoundError:
        # Dummy verification to prevent timing attacks
        verify_password(form_data.password, DUMMPY_PASSWORD)
        raise unauthenticated_exception
    if not verify_password(form_data.password, user.hashed_password):
        raise unauthenticated_exception
    return user
