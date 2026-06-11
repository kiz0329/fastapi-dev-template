from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Body, Security
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from ..database import AsyncSession, get_db_session
from ..service.signing import register_user, authenticate_user, delete_user as delete_user_service
from ..service.token import provide_tokens, reprovide_access_token
from ..schema.auth import Token, RefreshToken, Sign
from ..service.currentuser import get_current_user, TokenData
from ..system.const import (
    SUPERIOR_ACCESS_SCOPE,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    model = await authenticate_user(
        form_data,
        db_session
    )
    return await provide_tokens(model, db_session)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token_data: Annotated[RefreshToken, Body()],
    current_user: Annotated[TokenData, Security(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    return await reprovide_access_token(refresh_token_data.refresh_token, db_session)


@router.post("/append", response_model=Sign)
async def sign_up(
    sign_data: Annotated[Sign, Depends()],
    current_user: Annotated[TokenData,
                            Security(get_current_user, scopes=[SUPERIOR_ACCESS_SCOPE])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    _ = await register_user(
        sign_data.username,
        sign_data.password,
        db_session
    )
    return sign_data


@router.delete("/delete", response_model=Sign)
async def delete_user(
    sign_data: Annotated[Sign, Depends()],
    current_user: Annotated[TokenData,
                            Security(get_current_user, scopes=[SUPERIOR_ACCESS_SCOPE])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    _ = await delete_user_service(
        sign_data.username,
        db_session
    )
    return sign_data
