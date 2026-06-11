from datetime import datetime, timezone
from sqlalchemy import select
from .base import CRUDBase
from ..database import AsyncSession
from ..model.refreshtoken import RefreshToken
from ..schema.refreshtoken import RefreshTokenUploadSchema, RefreshTokenQuerySchema
from ..system.error import ResourceNotFoundError


class RefreshTokenCRUD(CRUDBase[RefreshToken, RefreshTokenUploadSchema, RefreshTokenQuerySchema]):
    async def prune_expired_tokens(self, current_time: datetime, db_session: AsyncSession):
        stmt = select(self._model).where(self._model.expire_at < current_time)
        result = await db_session.execute(stmt)
        expired_tokens = result.scalars().all()
        return expired_tokens

    async def get_by_token(self, token: str, db_session: AsyncSession):
        stmt = select(self._model).where(self._model.token == token)
        result = await db_session.execute(stmt)
        model=result.scalar_one_or_none()
        if not model:
            raise ResourceNotFoundError("Refresh token not found")
        return model


crud = RefreshTokenCRUD(RefreshToken)
