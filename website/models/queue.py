from website.models.master import Model
from website.models.users import User

class Queue(Model):
    mtype = 'queue'
    tablename = 'queues'

    @staticmethod
    def get_active_admin_queue(user_id):
        all_admin_queues = Queue.get(by="user_id", value=user_id)
        active = ""
        return False


    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, user_id, data, category, title)
        VALUES
            (%s, %s, %s, %s, %s)
        """)

        insertions = [
            model._id, model.user_id,
            model.data,
            model.category, model.title
        ]
        
        return statement, insertions
    
    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            user_id varchar(30) UNIQUE,
            data text,
            category varchar(50),       
            title text,
            processing int DEFAULT 0,
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
            category = %s,
            title = %s,
            processing = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s
        """)

        updates = [
            model.data, model.category,
            model.title, model.processing,
            model._id
        ]

        return statement, updates


    def __init__(self, mdict):
        super().__init__(mdict)
        self.user_id = mdict['user_id']
        self.data = mdict['data']
        self.category = mdict['category']
        self.title = mdict['title']
        self.processing = mdict['processing']

    @property
    def as_dict(self):
        return {
            '_id' : self._id,
            'data' : self.data,
            'category' : self.category,
            'title' : self.title,
            'processing' : self.processing,
        }

    @property
    def data_as_list(self):
        return self.data.split('$')

    def remove_user(self, user_id):
        """
        removes a user from the queue.
        true is returned if the action is
        successful, false if failure.
        """
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
        """
        adds a user to the queue.
        true is returned if the action is
        successful, false if failure or if
        the user is not in the list.
        """
        data_list = self.data.split('$')
        if user_id in data_list:
            return False
        else:
            self.data += f"{user_id}$"
            Queue.update(self)
            return True

    def get_user_position(self, user_id):
        """
        returns the position of a user
        in the data.
        """
        data_list = self.data.split('$')
        position = data_list.index(user_id)
        return position

    def get_next_opening(self):
        """
        checks how long the line
        is and returns the next open position.
        """
        list_len = len(self.data.split("$"))
        return list_len
        

    def data_as_users(self):
        """
        returns the data as users.
        """
        user_ids = self.data.split("$")
        users = [User.get(by="_id", value=_id)
            for _id in user_ids
            if _id]
        return users    

    
    def has_user(self, user_id):
        """
        returns true if a user is in the line.
        """
        data_list = self.data.split('$')
        if user_id in data_list:
            return True
        return False

    def get_processing_user(self):
        """
        returns which user is being processed
        based on current data and current processing
        value
        """
        data_list = self.data.split('$')
        user_id = data_list[self.processing]

        user = User.get(by='_id', value=user_id)

        if user:
            return user
        return False


    def __str__(self):
        return (f"""
        _id : {self._id}
        user_id : {self.user_id}
        data : {self.data}
        category : {self.category}
        title : {self.title}
        active : {self.active}
        processing : {self.processing}

        upload date : {self.upldate}
        last modified : {self.moddate}
        
        """)