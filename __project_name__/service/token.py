from typing import Annotated, Optional, Any
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
import ssl
from ..crud import refreshtoken_crud
from ..database import SessionDep
from ..model.user import User
from ..schema.refreshtoken import RefreshTokenUploadSchema
from ..model.refreshtoken import RefreshToken as RefreshTokenModel
from ..schema.token import Token
from ..service.scope import AccessLevel, generate_access_level_scopes
from ..system.const import SHORT_TEXT_LENGTH
from ..system.error import ResourceNotFoundError, UniqueConstraintError
from ..system.const import JWT_ALGORITHM, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS


#


class TokenData(BaseModel):
    username: Annotated[
        str,
        Field(max_length=SHORT_TEXT_LENGTH)
    ]
    scopes: Annotated[
        list[str],
        Field(max_length=SHORT_TEXT_LENGTH)
    ] = []


async def generate_tokens(user: User, db_session: SessionDep) -> Token:
    access_level = AccessLevel(user.access_level)
    data = {
        "sub": user.username,
        "scopes": " ".join(generate_access_level_scopes(access_level)),
    }
    return Token(
        access_token=create_access_token(data),
        refresh_token=await create_refresh_token(user.id, db_session),
        token_type="bearer"
    )


async def regenerate_tokens(refresh_token: str, db_session: SessionDep) -> Token:
    await refreshtoken_crud.prune_expired_tokens(datetime.now(timezone.utc), db_session)
    try:
        model = await refreshtoken_crud.get_by_token(refresh_token, db_session)
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = model.user
    access_level = AccessLevel(user.access_level)
    data = {
        "sub": user.username,
        "scopes": " ".join(generate_access_level_scopes(access_level)),
    }
    model = await rotate_refresh_token(model, db_session)
    return Token(
        access_token=create_access_token(data),
        refresh_token=model.token,
        token_type="bearer"
    )


# Access token


def create_token(data: dict[str, Any], expires_delta: timedelta):
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    expire = now_utc + expires_delta
    to_encode.update({"exp": expire, "iat": now_utc})
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict[str, Any], expires_delta: timedelta = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)):
    return create_token(data, expires_delta)


def verify_token(token: str):
    unauthenticated_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        scope_str = str(payload.get("scopes", ""))
        if username is None:
            raise unauthenticated_exception
        return TokenData(
            username=username,
            scopes=scope_str.split()
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise unauthenticated_exception


# Refresh token


async def create_refresh_token(user_id: int, db_session: SessionDep, *, expire_at: Optional[datetime] = None):
    token = ssl.RAND_bytes(32).hex()
    refresh_token = RefreshTokenUploadSchema(
        token=token,
        expire_at=(expire_at
                   or datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)),
        user_id=user_id
    )
    await refreshtoken_crud.create(refresh_token, db_session)
    return token


async def rotate_refresh_token(model: RefreshTokenModel, db_session: SessionDep) -> RefreshTokenModel:
    try:
        for _ in range(5):  # Try up to 5 times to generate a unique token
            try:
                model.token = ssl.RAND_bytes(32).hex()
                await db_session.commit()
                break
            except UniqueConstraintError:
                await db_session.rollback()

    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rotate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await db_session.refresh(model)
    return model
