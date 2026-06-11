from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from ..database import SessionDep
from ..model.user import User
from ..schema.user import UserUploadSchema, UserResponseSchema
from ..schema.token import Token, RefreshToken
from ..crud import refreshtoken_crud, user_crud
from ..system.const import AccessLevel, ADMIN_SCOPE
from ..system.error import ResourceNotFoundError
from ..service.token import generate_tokens, regenerate_tokens, TokenData
from ..service.account import modify_user_access_level
from ..service.authorization import get_current_user
from ..service.authentication import authenticate_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token")
async def sign_in(
        user: Annotated[
            User,
            Depends(authenticate_user)
        ],
        db_session: SessionDep
):
    return await generate_tokens(user, db_session)


@router.post("/refresh")
async def refresh_token(
        refresh_token_data: Annotated[RefreshToken, Body()],
        db_session: SessionDep
):
    return await regenerate_tokens(refresh_token_data.token, db_session)


@router.post("/signout", response_model=UserResponseSchema)
async def sign_out(
    refresh_token_data: Annotated[RefreshToken, Body()],
    db_session: SessionDep,
    token_data: Annotated[TokenData, Security(get_current_user, scopes=[])],
):
    model = await refreshtoken_crud.get_by_token(refresh_token_data.token, db_session)
    if model.user.username != token_data.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await refreshtoken_crud.delete(model.id, db_session)
    return model.user


@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user: Annotated[UserUploadSchema, Body()],
    db_session: SessionDep
):
    return await user_crud.create(user, db_session)


@router.put("/{user_id}", response_model=UserResponseSchema)
async def change_access_level(
    user_id: Annotated[int, Path(description="The ID of the user to modify")],
    access_level: Annotated[AccessLevel, Query(description="The new access level for the user")],
    token_data: Annotated[
        TokenData,
        Security(get_current_user,
                 scopes=[ADMIN_SCOPE])
    ],
    db_session: SessionDep,
):
    try:
        modified_user = await modify_user_access_level(user_id, access_level, db_session)
    except ResourceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return modified_user


@router.get("/", response_model=list[UserResponseSchema])
async def get_users(
    token_data: Annotated[
        TokenData,
        Security(get_current_user, scopes=[])
    ],
    db_session: SessionDep,
):
    return await user_crud.get_list(db_session)
