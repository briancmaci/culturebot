from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, URL
from aquabot.models import User, AdditionalFact, TagButton







