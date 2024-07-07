from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.memes import queryes
from memes import schemas
from app.database import get_db
from typing import List
from app.main import app


@app.get("/memes", response_model=List[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = queryes.get_memes(db, skip=skip, limit=limit)
    return memes


@app.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = queryes.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@app.post("/memes", response_model=schemas.Meme, status_code=status.HTTP_201_CREATED)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return queryes.create_meme(db=db, meme=meme)


@app.put("/memes/{meme_id}", response_model=schemas.Meme)
def update_meme(meme_id: int, meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return queryes.update_meme(db=db, meme_id=meme_id, meme=meme)


@app.delete("/memes/{meme_id}", response_model=schemas.Meme)
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    return queryes.delete_meme(db=db, meme_id=meme_id)
