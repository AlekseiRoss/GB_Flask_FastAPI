from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
# pip install email-validator


class RegisterForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(min=6, max=30)])
    last_name = StringField('Last Name',
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=30)])
    equal_password = PasswordField('Equal Password',
                                   validators=[DataRequired(),
                                               EqualTo('password'),
                                               Length(min=6, max=30)])
