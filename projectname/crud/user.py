from sqlalchemy import select
from .abc import UserCRUDBase
from ..database import SessionDep
from ..model.user import User
from ..schema.user import UserUploadSchema, UserQuerySchema
from ..system.error import ResourceNotFoundError


class UserCRUD(UserCRUDBase[User, UserUploadSchema, UserQuerySchema]):
    pass


crud = UserCRUD(User)
