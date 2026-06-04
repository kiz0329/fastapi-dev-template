from .base import CRUDBase
from ..models.user import User
from ..schemas.user import UserUploadSchema, UserQuerySchema


class UserCRUD(CRUDBase[User, UserUploadSchema, UserQuerySchema]):
    pass


crud = UserCRUD(User)
