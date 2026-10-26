from pathlib import Path
from os import listdir, mkdir
from re import sub
from zipfile import ZipFile

def consume_zip_folder(folder: Path):
    STAGED_FOLDER = Path("./transform/staged")/sub(string=folder.stem, pattern=r"^ZIP", repl="UNZIP") #replace("ZIP", "UNZIP")
    if not STAGED_FOLDER.exists():
        mkdir(STAGED_FOLDER)
    for file in listdir(folder):
        if file.endswith(".zip"):
            ZipFile(file=folder/file).extractall(
                path=STAGED_FOLDER/file.replace(".zip", "")
            )
    return STAGED_FOLDER
