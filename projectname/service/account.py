from fastapi import HTTPException, status
from .scope import AccessLevel, generate_access_level_scopes
from ..database import AsyncSession
from ..service.password import hash_password
from ..schema.user import UserUploadSchema, UserResponseSchema, UnhashedUserUploadSchema
from ..crud import user_crud
from ..system.error import ResourceNotFoundError


async def register_user(user_data: UnhashedUserUploadSchema, db_session: AsyncSession):
    attributes = user_data.model_dump(exclude={"password"})
    attributes.update({"hashed_password": hash_password(user_data.password)})
    new_user = UserUploadSchema.model_validate(attributes)
    created_user = await user_crud.create(new_user, db_session)
    return created_user


async def expel_user(username: str, db_session: AsyncSession):
    user = await user_crud.get_by_username(username, db_session)
    await user_crud.delete(user.id, db_session)


async def modify_user_access_level(user_id: int, new_access_level: AccessLevel, db_session: AsyncSession):
    user = await user_crud.get_by_id(user_id, db_session)
    user.scopes = " ".join(generate_access_level_scopes(new_access_level))
    await db_session.commit()
    return user
