from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

class Create_Admin_Code(FlaskForm):
    code = StringField('Admin Code',
        validators= [
            Length(min=6, max=10),
            DataRequired()
        ],
        render_kw = {
            'placeholder' : 'Add a new code here',
        }

    )
    submit_admin_code = SubmitField('Submit')


class Delete_Inactive_Queues(FlaskForm):
    # routine
    pass

class Clear_Active_Queues(FlaskForm):
    submit_clear_queues = SubmitField('Submit')

class Delete_Admin(FlaskForm):
    admin_id = StringField('Administrator ID',
        validators=[
            DataRequired()
        ],
        render_kw = {
            'placeholder' : 'Admin IDs',
            'hidden' : 'true',
            'readonly' : 'true'
        }
    )
    submit_delete_admin = SubmitField('Delete')

class Create_Temporary_Page(FlaskForm):
    user_id = StringField('Temporary User ID',
        validators=[
            DataRequired(),
        ],
        render_kw = {
            'placeholder' : 'Temporary User ID',
        }    
    )
    queue_id = StringField('Queue ID',
        validators=[
            DataRequired(),
        ],
        render_kw = {
            'placeholder' : 'Queue ID',
        }
    )
    submit_create_temporary_page = SubmitField('Create Page')


class Create_Temporary_User(FlaskForm):
    pass