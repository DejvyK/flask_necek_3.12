from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class Create_Queue(FlaskForm):
    category = RadioField('Category',
        render_kw = {
            'placeholder' : 'choose one',
        }
    )

    title = StringField('Title',
        validators = [
            DataRequired(), Length(min=1, max=50)
        ],
        render_kw = {
            'placeholder' : 'make it descriptive',
        }
    )
    submit_create_queue = SubmitField('Create Queue')


class Delete_Queue(FlaskForm):
    queue_id = StringField('Queue ID',
        validators = [
            DataRequired(), Length(min=1, max=50)
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    submit_delete_queue = SubmitField('Delete Queue')



class Reactivate_Queue(FlaskForm):
    queue_id = StringField('Queue ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )

    submit_reactivate_queue = SubmitField('Reactivate Queue')

class Remove_User_From_Queue(FlaskForm):
    queue_id = StringField('Queue ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )
    user_id = StringField('User ID',
        validators = [
            DataRequired()
        ],
        render_kw = {
            'readonly' : 'true',
            'hidden' : 'true'
        }
    )

    submit_remove_user = SubmitField('Remove')