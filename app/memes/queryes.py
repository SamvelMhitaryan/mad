from fastapi import UploadFile
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.memes import models, schemas
import aiohttp


async def upload_file(file: UploadFile):
    async with aiohttp.ClientSession() as session:
        url = '<ручка upload во внутреннем сервисе media>'
        async with session.post(url, data={'file': file.file}) as response:
            return await response.json()


async def get_meme(db: AsyncSession, meme_id: int):
    stmt = select(models.Meme).where(models.Meme.id == meme_id)
    return await db.execute(stmt)


async def get_memes(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(models.Meme).offset(skip).limit(limit)
    return await db.execute(stmt)


async def create_meme(db: AsyncSession, meme: schemas.MemeCreate, file: UploadFile):
    upload_response = await upload_file(file)
    memes_data = meme.model_dump()
    memes_data['file_id'] = upload_response['id']
    db_meme = models.Meme(**memes_data)
    db.add(db_meme)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme


async def update_meme(db: AsyncSession, meme_id: int, meme: schemas.MemeCreate):
    stmt = (
        update(models.Meme)
        .where(models.Meme.id == meme_id)
        .values(**meme.model_dump())
        .returning(models.Meme)
    )
    result = await db.execute(stmt)
    await db.commit()
    return await result.scalar_one_or_none()


async def delete_meme(db: AsyncSession, meme_id: int):
    stmt = (
        delete(models.Meme)
        .where(models.Meme.id == meme_id)
        .returning(models.Meme)
    )
    result = await db.execute(stmt)
    await db.commit()
    return await result.scalar_one_or_none()
