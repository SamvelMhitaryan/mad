from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from memes import models, schemas


def get_meme(db: Session, meme_id: int):
    stmt = select(models.Meme).where(models.Meme.id == meme_id)
    return db.scalars(stmt).first()


def get_memes(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Meme).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_meme(db: Session, meme: schemas.MemeCreate):
    db_meme = models.Meme(**meme.model_dump())
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme_id: int, meme: schemas.MemeCreate):
    stmt = (
        update(models.Meme)
        .where(models.Meme.id == meme_id)
        .values(**meme.model_dump())
        .returning(models.Meme)
    )
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()


def delete_meme(db: Session, meme_id: int):
    stmt = (
        delete(models.Meme)
        .where(models.Meme.id == meme_id)
        .returning(models.Meme)
    )
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()
