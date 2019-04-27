from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField, DateTimeField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class BlogForm(FlaskForm):
    username = SelectField('Username', choices=[], coerce=int)
    content = TextAreaField('Content', validators=[DataRequired()], render_kw=dict(placeholder='Write your message here ... '))
    submit = SubmitField('Submit')

# class LoginForm(FlaskForm):
#     username = Select

    
    
