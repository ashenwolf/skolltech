from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from misc.forms import TagListField
from models import BlogPost, BlogCategory

class BlogPostForm(model_form(BlogPost, exclude=["author", "date_created", "image"])):
    teaser = TextAreaField(u'Teaser', [validators.optional(), validators.length(max=255)])
    tags   = TagListField(u'Tags', [validators.optional()])

class BlogCategoryForm(model_form(BlogCategory, exclude=["slug"])):
	pass
