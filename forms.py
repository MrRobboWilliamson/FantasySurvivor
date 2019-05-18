from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, TextAreaField, validators, BooleanField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, NoneOf
import sqlite3

# Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    # enforce integrity constraints 
    c.execute("PRAGMA foreign_keys=ON;")
    return c, conn

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
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
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
         
# logout form is just a button
class LogoutForm(FlaskForm):
    # content = TextAreaField('Edit message', validators=[DataRequired()])
    logout_btn = SubmitField('Logout')
    cancel_btn = SubmitField('Cancel')

# create team form
class CreateTeam(FlaskForm):
    teamname = StringField('Team name', validators=[DataRequired(), Length(min=2, max=20)], render_kw=dict(placeholder='Name team'))
    submit = SubmitField('Submit')



