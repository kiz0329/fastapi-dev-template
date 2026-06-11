from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field, ValidationError
import jwt
from jwt import InvalidTokenError
import ssl
from ..system.environment import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS
from ..model.usercredential import UserCredential
from ..schema.refreshtoken import RefreshTokenUploadSchema, RefreshTokenQuerySchema
from ..database import AsyncSession, get_db_session
from ..crud import refreshtoken_crud
from ..system.error import ResourceNotFoundError, UNAUTHORIZED_EXCEPTION
from ..schema.auth import Token


class TokenData(BaseModel):
    username: Annotated[
        str,
        Field(description="Username associated with the token")
    ]
    scopes: Annotated[
        list[str],
        Field(description="List of scopes/permissions associated with the token")
    ] = []


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


async def create_access_token(user_credential: UserCredential):
    return await run_in_threadpool(
        create_token,
        data={
            "sub": str(user_credential.user.id),
            "scopes": user_credential.scope
        },
        expires_delta=timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )


async def create_refresh_token(
        user_credential: UserCredential,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        *,
        expires_at: Optional[datetime] = None
):
    expires_delta = timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = ssl.RAND_bytes(64).hex()
    _ = await refreshtoken_crud.create(
        RefreshTokenUploadSchema(
            token=refresh_token,
            user_credential_id=user_credential.id,
            expires_at=expires_at or (
                datetime.now(timezone.utc) + expires_delta)
        ),
        db_session
    )
    return refresh_token


async def provide_tokens(
        user_credential: UserCredential,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        *,
        refresh_token_expires_at: Optional[datetime] = None
):
    return Token(
        access_token=await create_access_token(user_credential),
        refresh_token=await create_refresh_token(
            user_credential,
            db_session,
            expires_at=refresh_token_expires_at
        ),
        token_type="Bearer"
    )


async def revoke_refresh_token(
        refresh_token: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    try:
        await refreshtoken_crud.delete_by_token(refresh_token, db_session)
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )


async def reprovide_access_token(
        refresh_token: str,
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    rt_models = await refreshtoken_crud.query(
        RefreshTokenQuerySchema(token=refresh_token),
        db_session
    )
    if not rt_models:
        raise UNAUTHORIZED_EXCEPTION
    rt_model = rt_models[0]
    user_credential = rt_model.user_credential
    return await provide_tokens(
        user_credential,
        db_session,
        refresh_token_expires_at=rt_model.expires_at
    )


async def decode_access_token(token: str) -> TokenData:
    try:
        payload = await run_in_threadpool(
            jwt.decode,
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub", "")
        scopes: list[str] = str(payload.get("scopes", "")).split()
        return TokenData(username=user_id, scopes=scopes)
    except (InvalidTokenError, ValidationError):
        raise UNAUTHORIZED_EXCEPTION
