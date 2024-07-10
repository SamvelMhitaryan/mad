from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.memes.database import engine
from app.memes import models
from app.memes.routers import router

memes_app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

memes_app.router.lifespan = lifespan

memes_app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.memes.main:memes_app",
                host='127.0.0.1', port=8000, reload=True)
