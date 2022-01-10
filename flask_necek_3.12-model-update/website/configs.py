import json
from pathlib import Path

with open(Path("./website/public_config.json")) as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')

    MYSQL_USER = config.get('MYSQL_USER')
    MYSQL_PASSWORD = config.get('MYSQL_PASSWORD')
    MYSQL_HOST = config.get('MYSQL_HOST')
    MYSQL_DB = config.get('MYSQL_DB')

    MYSQL_CURSORCLASS = "DictCursor"