from contextlib import asynccontextmanager
from fastapi import FastAPI
from projectname.database import engine
from projectname.model.base import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
