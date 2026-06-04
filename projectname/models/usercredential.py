from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import User
from .base import DBModelBase
from ..system.const import SHORT_TEXT_LENGTH


class UserCredential(DBModelBase):
    __tablename__ = "user_credentials"

    # Define your user credential model fields here, for example:
    username: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )
    scopes: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=True
    )
    disabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    # Add any additional fields and relationships as needed
    user_id: Mapped[int] = mapped_column(
        nullable=False
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="credentials"
    )
