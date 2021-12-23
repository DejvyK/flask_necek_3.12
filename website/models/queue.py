from website.models.master import Model
from website.models.users import User

class Queue(Model):
    mtype = 'queue'
    tablename = 'queues'

    @classmethod
    def get_insert_statement(cls, model):
        statement = (f"""
        INSERT INTO {cls.tablename}
            (_id, user_id, data, active, category, title)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        """)

        insertions = [model._id, model.user_id,
            model.data, model.active,
            model.category, model.title]
        
        return statement, insertions
    
    @classmethod
    def get_table_statement(cls):
        statement = (f"""
        CREATE TABLE {cls.tablename}(
            _id varchar(30) PRIMARY KEY,
            user_id varchar(30),
            data text,
            category varchar(50),            
            title text,
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
            category = %s,
            title = %s,
            moddate = CURRENT_TIMESTAMP()
        WHERE
            _id = %s
        """)

        updates = [model.data, model.active,
            model.category, model.title,
            model._id]

        return statement, updates


    def __init__(self, mdict):
        super().__init__(mdict)
        self.data = mdict['data']
        self.active = mdict['active']
        self.user_id = mdict['user_id']
        self.category = mdict['category']
        self.title = mdict['title']

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

    def has_user(self, user_id):
        data_list = self.data.split('$')
        if user_id in data_list:
            return True
        return False
        # problem: discovering what queues user is in takes too much time
        # solution 1: keep track of two things:
            #a queues column in the user table will keep track of what queues the user is in
            #a data column in the queue table will keep track of what users the queue contains
            # con: lack of concurrency

        #solution 2: when a user needs to see what queues they're in, pull all queues, run queue.has_user, and append a list

    @staticmethod
    def get_active_admin_queue(user_id):
        all_admin_queues = Queue.get(by="user_id", value=user_id, getmany=True)
        active = ""
        for queue in all_admin_queues:
            if queue.active==1:
                return queue
        return False

    def __str__(self):
        return (f"""
        _id : {self._id}
        user_id : {self.user_id}
        active : {self.active}
        data : {self.data}
        category : {self.category}
        title : {self.title}

        upload date : {self.upldate}
        last modified : {self.moddate}
        
        """)