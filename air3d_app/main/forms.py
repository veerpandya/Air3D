from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from air3d_app.models import User, Requests

class ProfileForm(FlaskForm):
    """Form to create a public profile."""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    creation_date = DateField('Date Joined')
    submit = SubmitField('Submit')


class RequestForm(FlaskForm):
    """Form to create a request for a case review."""
    username = StringField('User Name',
        validators=[DataRequired()])
    email = StringField('Email Address',
        validators=[DataRequired(), Length(min=6)])
    description = TextAreaField('Detailed Description of Product Request (include size specifications)',
        validators=[DataRequired(), Length(min=10)])
    submission_date = DateField('Date Submitted')
    submit = SubmitField('Submit')

class DesignForm(FlaskForm):
    """Form to upload a design from an owner."""
    userame = StringField('User Name',
        validators=[DataRequired()])
    email = StringField('Email Address',
        validators=[DataRequired(), Length(min=6)])
    description = TextAreaField('Description of Product',
        validators=[DataRequired(), Length(min=10)])
    submission_date = DateField('Date Submitted')
    submit = SubmitField('Submit')
