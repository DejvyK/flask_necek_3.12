from website.models.master import Model


class AdminCode(Model):
    mtype = 'admincode'
    tablename = 'admincodes'

    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, code)
        VALUES
            (%s, %s)
        """)
        
        insertions = [model._id, model.code]

        return statement, insertions

    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            code varchar(100) NOT NULL,
            upldate datetime DEFAULT CURRENT_TIMESTAMP(),
            moddate datetime DEFAULT CURRENT_TIMESTAMP()
        )
        """)
        return statement


    @classmethod
    def get_update_statement(cls, model):
        statement = (f""" UPDATE {cls.tablename}
        SET
            code = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s
        """)

        updates = [model.code, model._id]
        return statement

    def __init__(self, mdict):
        super().__init__(mdict)
        self.code = mdict['code']
        
