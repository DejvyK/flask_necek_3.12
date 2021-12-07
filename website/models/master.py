from website import db
from secrets import token_hex
from datetime import datetime

class Model:
    mtype = 'model'
    tablename = None