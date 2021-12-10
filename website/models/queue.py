from website.models.master import Model
from website.models.users import User
"""
how should I work on this queue system?

1. a user logs in, creates an account.
2. from the homepage, a queue button will appear
3. add to queue adds user to the bottom of the queue list

4. from the queue list, they can see there own position in the list, #4, #2 etc.

5. on the backend, an administrator can control positioning
6. 
"""
class Queue(Model):
    mtype = 'queue'
    tablename = 'queues'

    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, user_id, data, active)
        VALUES
            (%s, %s, %s, %s)
        """)

        insertions = [model._id, model.user_id, model.data, model.active]
        
        return statement, insertions

    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            user_id varchar(30),
            data text,
            active int DEFAULT 0,
            upldate datetime DEFAULT CURRENT_TIMESTAMP(),
            moddate datetime DEFAULT CURRENT_TIMESTAMP(),
            FOREIGN KEY (user_id) REFERENCES users(_id)
                ON UPDATE CASCADE
        )
        """)

        return statement

    @classmethod
    def get_update_statement(cls, model):
        statement = (f""" UPDATE {cls.tablename}
        SET
            data = %s,
            active = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s
        """)

        updates = [model.data, model.active, model._id]
        return statement, updates


    def __init__(self, mdict):
        super().__init__(mdict)
        self.data = mdict['data']
        self.active = mdict['active']
        self.user_id = mdict['user_id']


    def remove_user(self, user_id):
        data_list = self.data.split('$')
        data_list.remove(user_id)
        self.data = "$".join(data_list)
        try:
            Queue.update(self)
            return True
        except Exception as err:
            print (err)
            return False



    def add_user(self, user_id):
        data_list = self.data.split('$')
        if user_id in data_list:
            return False
        else:
            self.data += f"{user_id}$"
            Queue.update(self)
            return True

    def add_user_to_position(self, user_id):
        pass

    def get_user_position(self, user_id):
        data_list = self.data.split('$')
        position = data_list.index(user_id)
        return position

    def get_next_opening(self):
        list_len = len(self.data.split("$"))
        return list_len

    def data_as_users(self):
        user_ids = self.data.split("$")
        users = [User.get(by="_id", value=_id)
            for _id in user_ids
            if _id != False]
        return users