from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSession, create_async_engine, async_sessionmaker
from ..system.environment import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


SessionDep = Annotated[
    AsyncSession,
    Depends(get_db_session)
]
