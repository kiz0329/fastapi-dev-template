from typing import Annotated, Any
from datetime import datetime, timedelta, timezone
import jwt
from jwt import encode, decode, PyJWTError
from ...system.environment import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_TOKEN_EXPIRE_DAYS
)


async def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    current_time = datetime.now(timezone.utc)
    expire = current_time + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": current_time
    })
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


async def create_access_token(data: dict[str, Any]) -> str:
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return await _create_token(data, expires_delta=access_token_expires)


async def create_refresh_token(data: dict[str, Any]) -> str:
    refresh_token_expires = timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    return await _create_token(data, expires_delta=refresh_token_expires)

