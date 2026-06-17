from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .abc import DBModelBase
from ..system.const import SHORT_TEXT_LENGTH

if TYPE_CHECKING:
    from .user import User


class RefreshToken(DBModelBase):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        unique=True,
        nullable=False
    )
    expire_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        "User",
    )
