from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.memes.database import engine
from app.media import models
from app.media.routers import router

media_app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

media_app.router.lifespan = lifespan

media_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.media.main:media_app",
                host='127.0.0.1', port=8000, reload=True)
