from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession, create_async_engine, async_sessionmaker
from ..system.environment import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=_AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


AsyncSession = Annotated[
    _AsyncSession,
    get_db_session()
]
