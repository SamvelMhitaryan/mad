from fastapi import UploadFile, File, HTTPException
from minio.error import S3Error

from app.main import app, bucket_name, client


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    try:
        client.put_object(
            bucket_name, file.filename, file.file, length=-1, part_size=10*1024*1024,
            content_type=file.content_type
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename}
