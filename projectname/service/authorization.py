from typing import Annotated
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from .token import verify_token, TokenData
from .scope import AccessLevel, get_access_level_scope

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        get_access_level_scope(AccessLevel.GUEST): "Guest access",
        get_access_level_scope(AccessLevel.MEMBER): "Member access",
        get_access_level_scope(AccessLevel.SUPERIOR): "Superior access",
        get_access_level_scope(AccessLevel.ADMIN): "Admin access",
        get_access_level_scope(AccessLevel.DEVELOPER): "Developer access",
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
