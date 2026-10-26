from minio import Minio
from pathlib import Path
from os import listdir, remove
from configparser import ConfigParser

def upload_zip_folder(config: ConfigParser, minio_client: Minio):
    # USING bucket for zip folders refered in config file as 'zip-bucket'
    ZIP_BUCKET = config.get("Buckets", "zip-bucket")
    # USING path of a folder of downloaded zip files
    ZIPS_PATH = Path("./minio_c/downloaded-zip")
    # EACH folder of zip files is stored into the 'zip-bucket'-refered bucket
    for folder in listdir(ZIPS_PATH):
        if Path(folder).suffix == '.zip':
            minio_client.fput_object(ZIP_BUCKET, folder, ZIPS_PATH/folder)
            remove(ZIPS_PATH/folder)
        elif Path(ZIPS_PATH/folder).is_dir():
            # print(ZIPS_PATH/folder)
            yield ZIPS_PATH/folder
