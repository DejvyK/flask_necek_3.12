from website.models.master import Model
from website.models.users import User

class Queue(Model):
    mtype = 'queue'
    tablename = 'queues'


    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, user_id, data, category, title, skip_users)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        """)

        insertions = [
            model._id, model.user_id,
            model.data, model.category,
            model.title, model.skip_users
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
            skip_users text,
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
            skip_users = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s
        """)

        updates = [
            model.data, model.category,
            model.title, model.processing,
            model.skip_users, model._id
        ]

        return statement, updates


    def __init__(self, mdict):
        super().__init__(mdict)
        self.user_id = mdict['user_id']
        self.data = mdict['data']
        self.category = mdict['category']
        self.title = mdict['title']
        self.processing = mdict['processing']
        self.skip_users = mdict['skip_users']

    @property
    def as_dict(self):
        return {
            '_id' : self._id,
            'data' : self.data,
            'category' : self.category,
            'title' : self.title,
            'processing' : self.processing,
            'skip_users' : self.skip_users,
        }

    @property
    def data_as_list(self):
        data_list = [elem for elem in self.data.split('$') if elem]
        return data_list

    @property
    def skipped_as_list(self):
        skip_list = [elem for elem in self.skip_users.split('$') if elem]
        return skip_list


    def remove_user(self, user_id):
        """
        removes a user from the queue.
        true is returned if the action is
        successful, false if failure.
        """
        data_list = self.data_as_list
        data_list.remove(user_id)
        self.data = "$".join(data_list)
        try:
            Queue.update(self)
            return True
        except Exception as err:
            print (err)
            return False

    def remove_skipped (self, user_id):
        skipped = self.skipped_as_list
        skipped.remove(user_id)
        self.skip_users = "$".join(skipped)
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
        list_len = len(self.data_as_list)
        return list_len
        

    def data_as_users(self):
        """
        returns the data as users.
        """
        users = [User.get(by="_id", value=_id)
            for _id in self.data_as_list
            if _id]
        return users    

    
    def has_user(self, user_id):
        """
        returns true if a user is in the line.
        """
        if user_id in self.data_as_list:
            return True
        return False

    def has_skipped(self, user_id):
        """
        returns true if a user is in the skipped data.
        """
        if user_id in self.skipped_as_list:
            return True
        return False

    
    def already_skipped(self, user_id):
        """
        returns true if a user is in skipped, AND
        if a user has been passed by self.processing.
        """
        if user_id in self.skipped_as_list:
            pos = self.get_user_position(user_id)

            if pos:
                if self.processing >= pos:
                    return True
                return False


    def requeue_user(self, user_id):
        """
        finds a user in the queue and moves them
        to the end of the line. in it's place (maybe) if a fixed
        id for a dummy or removed user (maybe just a string that says dummy )
        """
        pos = self.get_user_position(user_id)

        if pos:
            new_data = self.data_as_list
            new_data[pos] = "skipped$"
            self.data = "$".join(new_data)
            self.add_user(user_id)

    def get_processing_user(self):
        """
        returns which user is being processed
        based on current data and current processing
        value
        """
        try:
            user_id = self.data_as_list[self.processing]
            user = User.get(by='_id', value=user_id)
        except IndexError as err:
            print ('no users in the queue')
            return False

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
        skip : {self.skip_users}

        upload date : {self.upldate}
        last modified : {self.moddate}
        
        """)