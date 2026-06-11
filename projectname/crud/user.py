from sqlalchemy import select
from .base import CRUDBase
from ..database import SessionDep
from ..model.user import User
from ..schema.user import UserUploadSchema, UserQuerySchema
from ..system.error import ResourceNotFoundError


class UserCRUD(CRUDBase[User, UserUploadSchema, UserQuerySchema]):
    async def get_by_username(self, username: str, db_session: SessionDep):
        result = await db_session.execute(
            select(self._model).where(self._model.username == username)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFoundError(
                f"User with username '{username}' not found"
            )
        return user


crud = UserCRUD(User)
