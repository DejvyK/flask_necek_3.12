from flask_mysqldb import MySQL

class DB (MySQL):
    def __init__(self, app=None):
        super().__init__(app=app)

    def get(self, tablename, col='column', value='value', getrandom=False, getall=False, getmany=False):
        statement = (f"""SELECT * FROM {tablename}
        WHERE {col} = "{value}" """)

        if getrandom is True:
            statement = (f"""SELECT * FROM {tablename}
                        ORDER BY RAND() LIMIT 1""")

        elif getall is True:
            statement = (f""" SELECT * FROM {tablename} """)
            cur = self.connection.cursor ()
            cur.execute (statement)
            records = cur.fetchall ()
            return records

        
        if getmany is True:
            cur = self.connection.cursor ()
            cur.execute (statement)
            records = cur.fetchall ()
            return records
            
        cur = self.connection.cursor ()
        cur.execute (statement)
        record = cur.fetchone ()
        return record


    def create_table (self, statement):
        try:    
            cur = self.connection.cursor ()
            cur.execute (statement)
            self.connection.commit ()
        except Exception as err:
            print (err)


    def insert (self, statements):
        try:
            cur = self.connection.cursor ()
            cur.execute (statements[0], statements[1])
            self.connection.commit ()
        except Exception as err:
            print ('ERROR INSERTING INTO DATABASE: \n')
            print (err)

    def remove (self, model):
        statement = f"""DELETE FROM {model.tablename}
        WHERE _id = "{model._id}" """
        cur = self.connection.cursor ()
        cur.execute (statement)
        self.connection.commit()

    def update (self, statements):
        try:
            cur = self.connection.cursor()
            cur.execute (statements[0], statements[1])
            self.connection.commit ()
        except Exception as err:
            print ('ERROR UPDATING MODEL')
            print (err)



# CUSTOM QUERIES



    def distinct_queue_categories(self):
        statement = "SELECT DISTINCT category from queues"
        try:
            cur = self.connection.cursor()
            cur.execute(statement)
            records = cur.fetchall()
            categories = [record['category'] for record in records if record['category']]
            return categories
        except Exception as err:
            print ('ERROR')
            print (err)
            return False
        




    # def authorize(self, model):
    #     cur = self.connection.cursor()
    #     cur.execute("""
    #     UPDATE users
    #     SET
    #         email = %s,
    #         password = %s,
    #         moddate = CURRENT_TIMESTAMP(),
    #         auth = 1
    #     WHERE
    #         _id = %s
    #     """, (model.email, model.password, model._id))
    #     self.connection.commit()
