from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, FileField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from misc.forms import TagListField
from models import PortfolioProject, HomeProject

class PortfolioProjectForm(model_form(PortfolioProject, exclude=["author", "date_created", "image"])):
    tags = TagListField(u'Tags', [validators.optional()])

class HomeProjectForm(model_form(PortfolioProject, exclude=["author", "date_created", "image"])):
    tags = TagListField(u'Tags', [validators.optional()])
