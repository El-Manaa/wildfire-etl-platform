from load.upload_dataframe import load_to_minio, lazyframe_to_parquet
from minio_c.configc import open_config
from minio_c.minio_client import create_client
from transform.op_download import consume_zip_folder
from extract.op_upload import upload_zip_folder
from transform.dataframe_tr import get_lazyframe, prepare_all_tables, make_reg_dim

from datetime import date
from pathlib import Path

def main():
    minio_client = create_client()
    for folder in upload_zip_folder(
        minio_client=minio_client,
        config=open_config()
    ):
        staged_folder = consume_zip_folder(folder)
        lf = get_lazyframe(staged_folder)
        for table, table_lf in prepare_all_tables(lf):
            parquet_path = lazyframe_to_parquet(table_lf, dest=Path(f"load/ready_parquet/{table}_{date.today().strftime('%y%m%d')}.parquet"))
            load_to_minio(minio_client=minio_client, parquet_path=parquet_path)    

def test():
    ...
    minio_client = create_client()
    for folder in upload_zip_folder(
        minio_client=minio_client,
        config=open_config()
    ):
        staged_folder = consume_zip_folder(folder)
        lf = get_lazyframe(staged_folder)
        reg_lf = make_reg_dim(lf)
        print(reg_lf.head(20).collect())

# main()
test()
