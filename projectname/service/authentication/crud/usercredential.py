from .base import CRUDBase
from ..model.usercredential import UserCredential
from ..schema.usercredential import (
    UserCredentialUploadSchema,
    UserCredentialQuerySchema,
)


class UserCredentialCRUD(CRUDBase[
    UserCredential,
    UserCredentialUploadSchema,
    UserCredentialQuerySchema,
]):
    pass


crud = UserCredentialCRUD(UserCredential)
