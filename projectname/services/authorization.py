from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db_session, Session
from .password import verify_password, hash_password
from ..crud import usercredential_crud
from ..schemas.usercredential import UserCredentialQuerySchema, UserCredentialInDBSchema


UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

_DUMMY_PASSWORD_HASH = hash_password("dummy_password")


async def get_user(username: str, db_session: Annotated[Session, Depends(get_db_session)]) -> UserCredentialInDBSchema | None:
    user_credentials = await usercredential_crud.query(
        UserCredentialQuerySchema(username=username),
        db_session
    )
    if not user_credentials:
        return None
    return UserCredentialInDBSchema.model_validate(user_credentials[0])


async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(get_db_session)]
) -> UserCredentialInDBSchema | None:
    username = form_data.username
    password = form_data.password
    user_credential = await get_user(username, db_session)
    if not user_credential:
        verify_password(password, _DUMMY_PASSWORD_HASH)
        return None
    if not verify_password(password, user_credential.password_hash):
        return None
    return user_credential
