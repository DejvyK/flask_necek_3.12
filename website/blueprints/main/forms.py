from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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
    submit_add_user_to_queue = SubmitField('Submit')


