from wtforms import SelectField, StringField, FloatField, URLField, IntegerField, TextAreaField, BooleanField,EmailField,PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Email


class RegisterForm(FlaskForm):
    """Form for registering users."""

    username = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("email", validators=[InputRequired()])
    first_name = StringField("first_name", validators=[InputRequired()])
    last_name = StringField("last_name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in users."""

    username = StringField("Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """Form for logging out users."""

class AddNoteForm(FlaskForm):
    """Form for adding notes."""

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content" ,validators=[InputRequired()])

class UpdateNoteForm(FlaskForm):
    """Form for updating notes."""

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content" ,validators=[InputRequired()])

