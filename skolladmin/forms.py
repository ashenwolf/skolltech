from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, validators
from wtforms.widgets import TextInput
import json

class SiteSettingsForm(Form):
    about_us_short = TextAreaField(u'About Us Short', [validators.optional(), validators.length(max=512)])
    work_with_us_short = TextAreaField(u'Work With Us Short', [validators.optional(), validators.length(max=512)])

    about_us_page = TextAreaField(u'About Us', [validators.optional()])
    work_with_us_page = TextAreaField(u'Work With Us', [validators.optional()])
    contacts_page = TextAreaField(u'Contacts Page', [validators.optional()])

    address = TextAreaField(u'Address', [validators.optional()])

    our_facebook = TextField(u'Facebook', [validators.optional()])
    our_twitter = TextField(u'Twitter', [validators.optional()])
    our_googleplus = TextField(u'Google+', [validators.optional()])
    our_linkedin = TextField(u'LinkedIn', [validators.optional()])
