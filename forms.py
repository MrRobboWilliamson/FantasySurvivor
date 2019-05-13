from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField, DateTimeField, validators, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NoneOf
import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class BlogForm(FlaskForm):
    # username = SelectField('Username', choices=[], coerce=int)
    content = TextAreaField(validators=[DataRequired()], render_kw=dict(placeholder='Send message'))
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = SelectField('Username', choices=[], coerce=int)
    submit = SubmitField('Submit')

# class LoginForm(FlaskForm):
#     username = Select
class EditForm(FlaskForm):
    content = TextAreaField('Edit message', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel_btn = SubmitField('Cancel')

# delete form is just a button
class DelForm(FlaskForm):
    # content = TextAreaField('Edit message', validators=[DataRequired()])
    delete_btn = SubmitField('Delete')
    cancel_btn = SubmitField('Cancel')

class CreateTeam(FlaskForm):
    team_nm = StringField('Team name', validators=[DataRequired()], render_kw=dict(placeholder="Cool name here"))
    c1 = SelectField('Contestant 1', choices=[], coerce=int)
    c2 = SelectField('Contestant 2', choices=[], coerce=int)
    c3 = SelectField('Contestant 3', choices=[], coerce=int)
    c4 = SelectField('Contestant 4', choices=[], coerce=int)

    submit = SubmitField('Submit')
    
    def check_unique(self, member_ids):
        print("\n\nThis is from the form\n", member_ids, '\n\n')
        if len(member_ids) > len(list(set(member_ids))):
            raise ValidationError('Team members must be unique')
         
# logout form is just a button
class LogoutForm(FlaskForm):
    # content = TextAreaField('Edit message', validators=[DataRequired()])
    logout_btn = SubmitField('Logout')
    cancel_btn = SubmitField('Cancel')
