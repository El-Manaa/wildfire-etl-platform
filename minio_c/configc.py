from configparser import ConfigParser


def open_config() -> ConfigParser:
    config = ConfigParser()
    with open("minio_c/config.ini", "r") as f:
        config.read_file(f)
    return config

