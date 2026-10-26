from minio import Minio
from dotenv import dotenv_values

MINIO_KEYS = dotenv_values("minio_c/.env.minio")

def create_client() -> Minio:
    client = Minio(
        '{0}:{1}'.format(
            MINIO_KEYS.get("HOST"),
            MINIO_KEYS.get("PORT")
        ),
        access_key=MINIO_KEYS.get("ROOT_USER"),
        secret_key=MINIO_KEYS.get("ROOT_PASSWORD"),
        secure=False
    )
    return client
