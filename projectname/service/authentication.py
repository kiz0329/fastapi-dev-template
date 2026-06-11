from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..model.user import User
from ..database import SessionDep, get_db_session
from ..crud.user import crud as user_crud
from ..system.error import ResourceNotFoundError


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
        user = await user_crud.get_by_username_and_password(
            form_data.username,
            form_data.password,
            db_session
        )
    except ResourceNotFoundError:
        raise unauthenticated_exception
    return user
