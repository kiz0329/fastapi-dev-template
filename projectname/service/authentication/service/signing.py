from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import AsyncSession, get_db_session
from ...password import hash_password, verify_password
from ..crud import usercredential_crud
from ..schema.usercredential import UserCredentialUploadSchema, UserCredentialQuerySchema
from ..system import ResourceNotFoundError
from ..system.error import UNAUTHORIZED_EXCEPTION
from ..service.accesslevel import provide_access_level_scope_str, AccessLevel

_DUMMY_PASSWORD_HASH = hash_password("dummy_password")


async def register_user(
        username: str,
        password: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    password_hash = hash_password(password)
    user_credential = UserCredentialUploadSchema(
        username=username,
        password_hash=password_hash,
        scope=provide_access_level_scope_str(AccessLevel.GUEST)
    )
    return await usercredential_crud.create(user_credential, db_session)


async def _get_user_by_username(
        username: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    try:
        user_credentials = await usercredential_crud.query(
            UserCredentialQuerySchema(username=username),
            db_session
        )
        if not user_credentials:
            return None
        return user_credentials[0]
    except ResourceNotFoundError:
        raise UNAUTHORIZED_EXCEPTION
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def authenticate_user(
        form_data: OAuth2PasswordRequestForm,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user_credential = await _get_user_by_username(form_data.username, db_session)
    if user_credential is None:
        verify_password(form_data.password, _DUMMY_PASSWORD_HASH)
        raise UNAUTHORIZED_EXCEPTION
    if not verify_password(form_data.password, user_credential.password_hash):
        raise UNAUTHORIZED_EXCEPTION
    return user_credential


async def delete_user(
        username: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user_credential = await _get_user_by_username(username, db_session)
    if user_credential is None:
        raise UNAUTHORIZED_EXCEPTION
    try:
        await db_session.delete(user_credential)
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    await db_session.commit()
