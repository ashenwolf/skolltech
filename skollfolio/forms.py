from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, FileField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from models import PortfolioProject, HomeProject

import re

class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip().lower() for x in valuelist[0].split(',')]
        else:
            self.data = []

class PortfolioProjectForm(model_form(PortfolioProject, exclude=["author", "date_created", "image"])):
    tags = TagListField(u'Tags', [validators.optional()])

class HomeProjectForm(model_form(PortfolioProject, exclude=["author", "date_created", "image"])):
    tags = TagListField(u'Tags', [validators.optional()])
