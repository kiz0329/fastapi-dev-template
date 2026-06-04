from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import DBModelBase
from ..system.const import SHORT_TEXT_LENGTH


class User(DBModelBase):
    __tablename__ = "users"

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
