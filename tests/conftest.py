import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from __project_name__.model.abc import Base
from __project_name__.model.user import User
from __project_name__.database import get_db_session
from __project_name__.system.const import DATABASE_URL, DEVELOPER_USER_NAME, DEVELOPER_USER_PASSWORD, AccessLevel
from __project_name__.service.password import hash_password
from __project_name__.service.scope import generate_access_level_scopes
from __project_name__.service.token import TokenData


@pytest.fixture
async def db_session():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        result = await session.execute(select(User).where(User.username == DEVELOPER_USER_NAME))
        if not result.scalar_one_or_none():
            session.add(User(
                username=DEVELOPER_USER_NAME,
                hashed_password=hash_password(DEVELOPER_USER_PASSWORD),
                access_level=AccessLevel.DEVELOPER.value,
                first_name="Jane",
                last_name="Doe",
            ))
            await session.commit()

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def developer_user(db_session):
    result = await db_session.execute(select(User).where(User.username == DEVELOPER_USER_NAME))
    return result.scalar_one()


@pytest.fixture
def developer_token_data():
    scopes = generate_access_level_scopes(AccessLevel.DEVELOPER)
    return TokenData(username=DEVELOPER_USER_NAME, scopes=scopes)
