from flask_mysqldb import MySQL

class DB (MySQL):
    def __init__(self, app=None):
        super().__init__(app=app)