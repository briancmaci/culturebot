from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, URL
from aquabot.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AdditionalFactEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    is_long = BooleanField('This should span the entire post')


class TagButtonEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired(), URL(require_tld=False, message="Invalid Url")])


class PostFactForm(FlaskForm):
    header = StringField('Header', validators=[DataRequired()])
    image_url = StringField('Image Url', validators=[URL(require_tld=False, message="Invalid Image Url")])
    title = StringField('Main Title', validators=[DataRequired()])
    title_url = StringField('Main Title Url', validators=[URL(require_tld=False, message="Invalid Url")])
    body = TextAreaField('Body', validators=[DataRequired()])
    additional_facts = FieldList(FormField(AdditionalFactEntryForm), min_entries=1)
    tag_buttons = FieldList(FormField(TagButtonEntryForm), min_entries=1)
    submit = SubmitField('Post LGBTQ Fact')





