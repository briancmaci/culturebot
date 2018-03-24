from . import *
from flask_wtf import Form


class AdditionalFactEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    is_long = BooleanField('This should span the entire post')


class TagButtonEntryForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired(), URL(require_tld=False, message="Invalid Url")])


class PostFactForm(FlaskForm):
    header = StringField('Header', validators=[DataRequired()])
    thumb_url = StringField('Thumb Url', validators=[URL(require_tld=False, message="Invalid Image Url")])
    title = StringField('Main Title', validators=[DataRequired()])
    title_url = StringField('Main Title Url', validators=[URL(require_tld=False, message="Invalid Url")])
    description = TextAreaField('Main Description', validators=[DataRequired()])
    #additional_fact_field = FormField(AdditionalFactEntryForm, default=lambda: AdditionalFact())
    additional_facts = FieldList('Additional Facts', FormField(AdditionalFactEntryForm), min_entries=1)
    # tag_button_field = FormField(TagButtonEntryForm)
    # tag_buttons = FieldList('Button Tags', tag_button_field, min_entries=0)
    # tag_buttons.append_entry(tag_button_field)
    submit = SubmitField('Post LGBTQ Fact')