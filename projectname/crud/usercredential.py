from .base import CRUDBase
from ..models.usercredential import UserCredential
from ..schemas.usercredential import UserCredentialUploadSchema, UserCredentialQuerySchema


class UserCredentialCRUD(CRUDBase[UserCredential, UserCredentialUploadSchema, UserCredentialQuerySchema]):
    pass


crud = UserCredentialCRUD(UserCredential)
