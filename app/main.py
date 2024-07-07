from minio import Minio
from fastapi import FastAPI
import uvicorn

from app.database import engine
from app.memes import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "memes"


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
