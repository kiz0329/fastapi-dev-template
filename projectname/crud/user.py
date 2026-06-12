from .abc import UserCRUDBase
from ..model.user import User
from ..schema.user import UserUploadSchema, UserQuerySchema


class UserCRUD(UserCRUDBase[User, UserUploadSchema, UserQuerySchema]):
    pass


crud = UserCRUD(User)
