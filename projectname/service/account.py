from .scope import AccessLevel
from ..database import SessionDep
from ..crud import user_crud


async def expel_user(username: str, db_session: SessionDep):
    user = await user_crud.get_by_username(username, db_session)
    await user_crud.delete(user.id, db_session)


async def modify_user_access_level(user_id: int, new_access_level: AccessLevel, db_session: SessionDep):
    user = await user_crud.get_by_id(user_id, db_session)
    user.access_level = new_access_level.value
    await db_session.commit()
    return user
