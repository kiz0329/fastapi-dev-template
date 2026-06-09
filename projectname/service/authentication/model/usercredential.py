from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import DBModelBase
from ....system.const import SHORT_TEXT_LENGTH


if TYPE_CHECKING:
    from ....model.user import User


class UserCredential(DBModelBase):
    __tablename__ = "authentication__user_credentials"

    username: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False,
        unique=True,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )
    scope: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        uselist=False,
    )
