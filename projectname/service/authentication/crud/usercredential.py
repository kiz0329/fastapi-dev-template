from .base import CRUDBase
from ..model.usercredential import UserCredential
from ..schema.usercredential import (
    UserCredentialUploadSchema,
    UserCredentialQuerySchema,
)
from ..database import AsyncSession
from ..system.const import AccessLevel
from ..service.accesslevel import provide_access_level_scope_str


class UserCredentialCRUD(CRUDBase[
    UserCredential,
    UserCredentialUploadSchema,
    UserCredentialQuerySchema,
]):
    async def modify_access_level(self, access_level: AccessLevel, id: int, session: AsyncSession):
        model = await self.get_by_id(id, session)
        if model:
            model.scope = provide_access_level_scope_str(access_level)
            await session.commit()


crud = UserCredentialCRUD(UserCredential)
