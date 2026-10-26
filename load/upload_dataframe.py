from re import findall
from minio.datatypes import Bucket
from pathlib import Path
from polars import LazyFrame
from duckdb import connect, DuckDBPyConnection
from minio_c.configc import open_config
from minio_c.minio_client import create_client, Minio

def lazyframe_to_parquet(lf: LazyFrame, dest: Path) -> Path:
    lf.collect().write_parquet(file=dest)
    return dest

def load_to_minio(minio_client: Minio, parquet_path: Path):
    if bucket_prefix := findall(
        string = parquet_path.stem,
        pattern = r"""(time|date|reg|sat|hotspot)_(?:dim|fact)_(?:\d{6,12})"""
    ):
        bucket_name = open_config().get("Buckets", bucket_prefix[0] + "_bucket")
        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=parquet_path.name,
            file_path=parquet_path
        )
        ...
    
