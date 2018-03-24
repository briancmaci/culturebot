from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, URL
