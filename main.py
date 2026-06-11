from contextlib import asynccontextmanager
from fastapi import FastAPI
from projectname.database import engine
from projectname.model.abc import Base
from projectname.router import auth_router


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def ensure_developer_account():
    from sqlalchemy import select
    from projectname.database.session import AsyncSessionLocal
    from projectname.model.user import User
    from projectname.system.environment import DEVELOPER_USER_PASSWORD
    from projectname.system.const import DEVELOPER_USER_NAME
    from projectname.service.password import hash_password
    from projectname.service.scope import AccessLevel
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(
            select(User).where(User.username == DEVELOPER_USER_NAME)
        )
        user = result.scalar_one_or_none()

        def fill_developer_info(user: User):
            user.hashed_password = hash_password(DEVELOPER_USER_PASSWORD)
            user.access_level = AccessLevel.DEVELOPER.value
            user.first_name = "安治川"
            user.last_name = "鐵之助"

        if not user:
            user = User()
            fill_developer_info(user)
            db_session.add(user)
        else:
            fill_developer_info(user)
        await db_session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await ensure_developer_account()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
