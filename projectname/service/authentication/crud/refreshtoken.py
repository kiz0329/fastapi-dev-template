from datetime import datetime, timezone
from sqlalchemy import select
from .base import CRUDBase
from ..model.refreshtoken import RefreshToken
from ..schema.refreshtoken import (
    RefreshTokenUploadSchema,
    RefreshTokenQuerySchema,
)
from ..model.refreshtoken import RefreshToken
from ..database import AsyncSession
from ..system.error import ResourceNotFoundError


class RefreshTokenCRUD(CRUDBase[
    RefreshToken,
    RefreshTokenUploadSchema,
    RefreshTokenQuerySchema,
]):
    async def delete_by_token(self, token: str, db_session:  AsyncSession):
        result = await db_session.execute(
            select(self._model).where(self._model.token == token)
        )
        result = result.scalar_one_or_none()
        if result:
            await db_session.delete(result)
            await db_session.commit()
        else:
            raise ResourceNotFoundError(
                f"Refresh token not found: token = '{token}'"
            )

    async def prune_expired_tokens(self, db_session: AsyncSession):
        now = datetime.now(timezone.utc)
        result = await db_session.execute(
            select(self._model).where(self._model.expires_at < now)
        )
        expired_tokens = result.scalars().all()
        for token in expired_tokens:
            await db_session.delete(token)
        await db_session.commit()

crud = RefreshTokenCRUD(RefreshToken)
