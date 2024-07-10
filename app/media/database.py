from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.media.settings import DATABASE_URL_MEDIA

engine = create_async_engine(DATABASE_URL_MEDIA)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db_media():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
