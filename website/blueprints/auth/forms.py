from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class Authorize_User(FlaskForm):
    email = StringField('Email',
        validators = [
            DataRequired(), Email(),
            Length(min=4, max=50)
        ],
        render_kw = {
            'placeholder' : 'joejackson@gmail.com',
        }
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(), Length(min=8, max=50)
        ],
        render_kw = {
        }
    )
    submit_authorize_user = SubmitField('Login')


class Register_User(FlaskForm):
    fname = StringField('First Name',
        validators = [
            DataRequired(),
            Length(min=1, max=30)
        ],
        render_kw = {
            'placeholder' : 'First Name',
        }
    )

    lname = StringField('Last Name',
        validators = [
            DataRequired(),
            Length(min=1, max=30)
        ],
        render_kw = {
            'placeholder' : 'Last Name',
        }
    )

    email = StringField('Email',
        validators = [
            DataRequired(), Email(),
            Length(min=1, max=50)
        ],
        render_kw = {
            'placeholder' : 'joejackson@gmail.com',
        }
    )

    password = PasswordField('Password',
        validators = [
            DataRequired(), Length(min=1, max=50)
        ],
        render_kw = {
            'placeholder' : '8 characters or longer'
        }
    )

    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(), Length(min=1, max=50),
            EqualTo('password')
        ],
        render_kw = {
            'placeholder' : 'must match original password'
        }
    )

    admincode = StringField('Admin Code',
        validators = [
            Length(min=1, max=30)
        ],
        render_kw = {
            'placeholder' : '(Optional)',
        }
    )

    submit_register_user = SubmitField('Register')


