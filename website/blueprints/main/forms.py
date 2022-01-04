from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Add_User_To_Queue(FlaskForm):
    user_id = StringField('User ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    queue_id = StringField ('Queue ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    submit_add_user_to_queue = SubmitField('Join Queue')

class Leave_Queue(FlaskForm):
    user_id = StringField('User ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    queue_id = StringField ('Queue ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    submit_leave_queue = SubmitField('Leave Queue')

class Rejoin_Queue(FlaskForm):
    user_id = StringField('User ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    queue_id = StringField ('Queue ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    submit_rejoin_queue = SubmitField('Rejoin Queue')


class Search_Bar(FlaskForm):
    query = StringField('Find a Queue',
        validators= [
            Length(min=2, max=15),
            DataRequired()
        ],
        render_kw = {
            'placeholder' : 'search',

        }
    )
    submit_search_bar = SubmitField('Search')
