from flask_login import UserMixin
from website import login_manager
from website.models.master import Model


@login_manager.user_loader
def load_user(_id):
    return User.get(by="_id", value=_id)

class User(Model, UserMixin):
    mtype = 'user'
    tablename = 'users'

    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, email, fname, lname, password)
        VALUES
            (%s, %s, %s, %s, %s)
        """)
        
        insertions = [model._id, model.email,
            model.fname, model.lname, model.password]

        return statement, insertions


    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            email varchar(30) NOT NULL UNIQUE,
            fname varchar(30),
            lname varchar(30),
            password varchar(100) NOT NULL,
            upldate datetime DEFAULT CURRENT_TIMESTAMP(),
            moddate datetime DEFAULT CURRENT_TIMESTAMP()
        )
        """)
        return statement

    @classmethod
    def get_update_statement(cls, model):
        statement = (f""" UPDATE {cls.tablename}
        SET
            email = %s,
            fname = %s,
            lname = %s,
            password = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            id = %s,
        """)

        updates = [model.email, model.fname,
            model.lname, model.password]

        return statement

    def __init__(self, mdict):
        super().__init__(mdict)
        self.email = mdict['email']
        self.fname = mdict['fname']
        self.lname = mdict['lname']
        self.password = mdict['password']


    @property
    def as_dict(self):
        return {
            "_id" : self._id,
            "email" : self.email,
            "fname" : self.fname,
            "lname" : self.lname,
            "moddate" : self.moddate,
            "upldate" : self.upldate,
        }
    

    