from .base import CRUDBase
from ..model.user import User
from ..schema.user import UserUploadSchema, UserQuerySchema


class UserCRUD(CRUDBase[User, UserUploadSchema, UserQuerySchema]):
    pass


crud = UserCRUD(User)
