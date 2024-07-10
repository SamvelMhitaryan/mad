from minio import Minio

from app.media.settings import MINIO_ENDPOINT, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, MINIO_SECURE, MINIO_BUCKET_NAME


client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=MINIO_SECURE
)

bucket_name = MINIO_BUCKET_NAME
