from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from misc.forms import TagListField

from models import StaticPage


class SiteSettingsForm(Form):
    about_us_short = TextAreaField(u'About Us Short', [validators.optional(), validators.length(max=512)])

    work_with_us_short = TextAreaField(u'Work With Us Short', [validators.optional(), validators.length(max=512)])
    work_with_us_page = TextAreaField(u'Work With Us', [validators.optional()])

    address = TextAreaField(u'Address', [validators.optional()])

    our_facebook = TextField(u'Facebook', [validators.optional()])
    our_twitter = TextField(u'Twitter', [validators.optional()])
    our_googleplus = TextField(u'Google+', [validators.optional()])
    our_linkedin = TextField(u'LinkedIn', [validators.optional()])


class StaticPageForm(model_form(StaticPage)):
    tags = TagListField(u'Tags', [validators.optional()])
