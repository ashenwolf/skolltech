from wtforms import Form
from wtforms import Field, BooleanField, TextField, TextAreaField, FileField, SelectMultipleField, validators
from wtforms.widgets import TextInput
from wtforms.ext.appengine.db import model_form
from google.appengine.ext import db
from misc.forms import TagListField
from models import PortfolioProject, HomeProject, ProjectCategory, Technology

PortfolioProjectFormBase = model_form(PortfolioProject, exclude=["author", "date_created", "image"])

class KeyListField(SelectMultipleField):
    def __init__(self, label='', validators=None, ref_class=None, **kwargs):
        super(KeyListField, self).__init__(label, validators, **kwargs)
        self.ref_class = ref_class

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and self.coerce(value) in [x.id() for x in self.data]
            yield (value, label, selected)

    def process_data(self, value):
        try:
            self.data = value
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(db.Key.from_path(self.ref_class, self.coerce(x)) for x in valuelist)
        except ValueError:
            raise ValueError(self.gettext(u'Invalid choice(s): one or more data inputs could not be coerced'))

    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            for d in self.data:
                if d.id() not in values:
                    raise ValueError(self.gettext(u"'%(value)s' is not a valid choice for this field") % dict(value=d))


class PortfolioProjectForm(PortfolioProjectFormBase):
    tags = TagListField(u'Tags', [validators.optional()])
    technologies = KeyListField(u'Technologies', [validators.optional()], coerce=long, ref_class='Technology')

#    def process(zelf, formdata=None, obj=None, **kwargs):
#       super(PortfolioProjectFormBase, self).process(formdata, obj, **kwargs)
#       tech = self._fields["technologies"]

class HomeProjectForm(model_form(PortfolioProject, exclude=["author", "date_created", "image"])):
    tags = TagListField(u'Tags', [validators.optional()])

class ProjectCategoryForm(model_form(ProjectCategory, exclude=["slug"])):
    pass

class TechnologyForm(model_form(Technology, exclude=["slug"])):
    pass
