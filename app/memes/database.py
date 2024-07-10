from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.memes.settings import DATABASE_URL_MEMES

engine = create_async_engine(DATABASE_URL_MEMES)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db_memes():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
