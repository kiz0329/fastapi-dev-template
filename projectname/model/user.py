from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import DBModelBase
from ..system.const import SHORT_TEXT_LENGTH, AccessLevel
from ..service.scope import generate_access_level_scopes


class User(DBModelBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )
    scopes: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False,
        default=" ".join(generate_access_level_scopes(AccessLevel.GUEST))
    )

    # Define your user model fields here, for example:
    first_name: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        nullable=False
    )

    # Add any additional fields and relationships as needed
