from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from jwt import InvalidTokenError
from pydantic import ValidationError
from .typing import TokenData
from ..authorization import get_user
from ...database import Session, get_db_session
from ...schemas.usercredential import UserCredentialInDBSchema
from ...system.environment import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="sign-in",
    scopes={
        "member": "Allows access to member-only resources",
        "senior": "Allows access to senior-only resources",
        "admin": "Allows access to admin-only resources",
        "developer": "Allows access to developer-only resources"
    }
)


async def get_current_user(
        security_scopes: SecurityScopes,
        db_session: Annotated[Session, Depends(get_db_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authentication_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authentication_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": authentication_value},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope = payload.get("scope", "")
        token_scopes = scope.split()
        token_data = TokenData(username=username, scopes=token_scopes)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = await get_user(token_data.username, db_session=db_session)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authentication_value},
            )
    return user


async def get_current_active_user(
        current_user: Annotated[UserCredentialInDBSchema,
                                Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
