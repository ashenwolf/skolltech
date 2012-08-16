from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from models import BlogPost

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

class BlogPostForm(model_form(BlogPost, exclude=["author", "date_created", "image"])):
    teaser = TextAreaField(u'Teaser', [validators.optional(), validators.length(max=255)])
    tags   = TagListField(u'Tags', [validators.optional()])
