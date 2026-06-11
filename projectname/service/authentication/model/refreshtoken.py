from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import DBModelBase
from ..system.const import SHORT_TEXT_LENGTH


if TYPE_CHECKING:
    from .usercredential import UserCredential


class RefreshToken(DBModelBase):
    __tablename__ = "authentication__refresh_tokens"

    token: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False,
        unique=True,
        index=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    user_credential_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("authentication__user_credentials.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_credential: Mapped["UserCredential"] = relationship(
        "UserCredential",
        uselist=False,
    )
