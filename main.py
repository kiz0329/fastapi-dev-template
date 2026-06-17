from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware import Middleware
from __project_name__.database import engine
from __project_name__.model.abc import Base
from __project_name__.router import auth_router
from __project_name__.system.error import CRUDErrorBase


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def ensure_developer_account():
    from sqlalchemy import select
    from __project_name__.database.session import AsyncSessionLocal
    from __project_name__.model.user import User
    from __project_name__.system.const import DEVELOPER_USER_PASSWORD
    from __project_name__.system.const import DEVELOPER_USER_NAME
    from __project_name__.service.password import hash_password
    from __project_name__.service.scope import AccessLevel
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


@app.exception_handler(CRUDErrorBase)
async def crud_error_handler(request, exc: CRUDErrorBase):
    http_exception = HTTPException(
        status_code=exc.http_status,
        detail=exc.args
    )
    return await http_exception_handler(request, http_exception)

app.include_router(auth_router)
