from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from .token import verify_token, TokenData
from ..system.const import (
    GUEST_SCOPE,
    MEMBER_SCOPE,
    SUPERIOR_SCOPE,
    ADMIN_SCOPE,
    DEVELOPER_SCOPE,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        GUEST_SCOPE: "Guest access",
        MEMBER_SCOPE: "Member access",
        SUPERIOR_SCOPE: "Superior access",
        ADMIN_SCOPE: "Admin access",
        DEVELOPER_SCOPE: "Developer access",
    })


async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
    authenticate_value = (
        f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else
        "Bearer"
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        token_data = verify_token(token)
    except HTTPException:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return token_data
