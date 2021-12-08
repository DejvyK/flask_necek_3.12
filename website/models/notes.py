from website.models.master import Model

class Note(Model):
    mtype = "note"
    tablename = "notes"

    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, data, user_id)
        VALUES
            (%s, %s, %s)
        """)

        insertions = [model._id, model.data,
            model.user_id]

        return statement, insertions

    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            user_id varchar(30),
            data text,
            upldate datetime DEFAULT CURRENT_TIMESTAMP(),
            moddate datetime DEFAULT CURRENT_TIMESTAMP()
        )""")
        
        return statement


    @classmethod
    def get_update_statement(cls, model):
        statement = (f""" UPDATE {cls.tablename}
        SET
            data = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s,
        """)

        updates = [model.data, model._id]

        return statement, updates

    def as_dict(self):
        f_upldate = datetime.strftime(self.upldate, '%B %d %Y')
        f_moddate = datetime.strftime(self.moddate, '%B %d %Y')
        return {
            "_id" : self._id,
            "user_id" : self.user_id,
            "data" : self.data,
            "upldate" : f_upldate,
            "moddate" : f_moddate,
        }

    def as_json(self):
        return jsonify(self.as_dict())
