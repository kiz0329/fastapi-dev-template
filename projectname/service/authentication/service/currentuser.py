from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import InvalidTokenError
from pydantic import ValidationError
from .token import decode_access_token
from ..service.token import TokenData
from ..system.const import GUEST_ACCESS_SCOPE, MEMBER_ACCESS_SCOPE, SUPERIOR_ACCESS_SCOPE, ADMIN_ACCESS_SCOPE, DEVELOPER_ACCESS_SCOPE


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        GUEST_ACCESS_SCOPE: "Guest access",
        MEMBER_ACCESS_SCOPE: "Member access",
        SUPERIOR_ACCESS_SCOPE: "Superior access",
        ADMIN_ACCESS_SCOPE: "Admin access",
        DEVELOPER_ACCESS_SCOPE: "Developer access",
    }
)


async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    authenticate_value = (
        f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else
        "Bearer"
    )
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        token_data = await decode_access_token(token)
    except (InvalidTokenError, ValidationError):
        raise credential_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise credential_exception
    return token_data
