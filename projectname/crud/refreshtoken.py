from datetime import datetime
from sqlalchemy import select
from .abc import CRUDBase
from ..database import SessionDep
from ..model.refreshtoken import RefreshToken
from ..schema.refreshtoken import RefreshTokenUploadSchema, RefreshTokenQuerySchema
from ..system.error import ResourceNotFoundError


class RefreshTokenCRUD(CRUDBase[RefreshToken, RefreshTokenUploadSchema, RefreshTokenQuerySchema]):
    async def prune_expired_tokens(self, current_time: datetime, db_session: SessionDep):
        stmt = select(self._model).where(self._model.expire_at < current_time)
        result = await db_session.execute(stmt)
        expired_tokens = result.scalars().all()
        for token in expired_tokens:
            await db_session.delete(token)
        await db_session.commit()
        return expired_tokens

    async def get_by_token(self, token: str, db_session: SessionDep):
        stmt = select(self._model).where(self._model.token == token)
        result = await db_session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ResourceNotFoundError("Refresh token not found")
        return model


crud = RefreshTokenCRUD(RefreshToken)
