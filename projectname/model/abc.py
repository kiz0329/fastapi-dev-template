from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from ..system.const import SHORT_TEXT_LENGTH, AccessLevel
from ..service.scope import generate_access_level_scopes


class Base(DeclarativeBase):
    pass


class DBModelBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc))


class UserModelBase(DBModelBase):
    __abstract__ = True

    username: Mapped[str] = mapped_column(
        String(SHORT_TEXT_LENGTH),
        index=True,
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
