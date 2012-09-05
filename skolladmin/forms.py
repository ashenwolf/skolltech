from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from misc.forms import TagListField

from models import StaticPage


class SiteSettingsForm(Form):
	#about us
    about_us = TextAreaField(u'About Us', [validators.optional(), validators.length(max=512)])

    what_we_do = TextAreaField(u'What We Do', [validators.optional(), validators.length(max=512)])
    work_with_us = TextAreaField(u'Work With Us', [validators.optional(), validators.length(max=512)])
    hire_us = TextAreaField(u'Hire Us', [validators.optional(), validators.length(max=512)])

class SiteContactsForm(Form):
    # contacts
    address = TextAreaField(u'Address', [validators.optional()])

    our_facebook = TextField(u'Facebook', [validators.optional()])
    our_twitter = TextField(u'Twitter', [validators.optional()])
    our_googleplus = TextField(u'Google+', [validators.optional()])
    our_linkedin = TextField(u'LinkedIn', [validators.optional()])


class StaticPageForm(model_form(StaticPage)):
    tags = TagListField(u'Tags', [validators.optional()])
