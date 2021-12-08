from website import db
from secrets import token_hex
from datetime import datetime

class Model:
    mtype = 'model'
    tablename = None

    @classmethod
    def add (cls, model):
        """ Model.add(model) inserts a new model
        into the databse. """
        ModelObj = cls._Model__getobj ()
        statements = ModelObj.get_insert_statement (model)
        db.insert(statements)

    @classmethod
    def get (cls, by='', value='', getrandom=False, getall=False, getmany=False):
        """
        returns model object(s) 
        **by specifies the column to search

        **value specifies the value to search for in 'by'

        **getrandom=True always returns 1 random model from the table
        
        **getall=True returns all of the models in the table
        
        **getmany=True returns all of the models in the
                       table that match the query,
                       similar to fetchmany
        """
        ModelObj = cls._Model__getobj ()

        if getmany:
            records = db.get(ModelObj.tablename, col=by,
                        value=value, getmany=True)
            models = [ModelObj(record) for record in records]
            return models

        if getall:
            records = db.get(ModelObj.tablename, getall=True)
            models = [ModelObj(record) for record in records]
            return models


        record = db.get(ModelObj.tablename, col=by, value=value, getrandom=getrandom)

        if record is None:
            return None
        
        model = ModelObj (record)
        return model

    @classmethod
    def mk_table (cls):
        """ creates the model's
        complementary table """
        ModelObj = cls._Model__getobj ()
        mk_table_statement = ModelObj.get_table_statement()
        try:
            db.create_table (mk_table_statement)
            return True
        except Exception as err:
            print (err)
            return False

    @classmethod
    def update (cls, model):
        """ updates a model in the db.
        Model.update(model) where model
        already exists in the db. """
        ModelObj = cls._Model__getobj ()
        update_statement = ModelObj.get_update_statement (model)
        db.update(update_statement)


    @staticmethod
    def remove (model):
        """ model is deleted from the db,
        Model.remove(model) where model
        already exists in the db. """
        db.remove(model)

    @classmethod
    def __getobj (cls):
        return cls

#//SECTION: __init__
    def __init__(self, mdict):
        self._id = ""
        self.id = ""
        self.upldate = ""
        self.moddate = ""
        self.__checkdict (mdict)

    def __checkdict (self, mdict):
        try:
            self._id = mdict['_id']
            self.id = mdict ['_id']
        except Exception as err1:
            self._id = token_hex(8)
            self.id = self._id

        try:
            self.upldate = mdict ['upldate']
        except Exception as err3:
            pass

        try:
            self.moddate = mdict ['moddate']
        except Exception as err4:
            pass
