import datetime
from google.appengine.ext import db
from misc.forms import TagListField

class SiteSettings(db.Model):
    value = db.TextProperty()

    @classmethod
    def get(cls, key):
        try:
            return cls.get_by_key_name(key).value
        except:
            return ""

    @classmethod
    def set(cls, key, value):
        setting = cls.get_or_insert(key, value = value)
        setting.put()


    @classmethod
    def batch_set(cls, settings):
        new_settings = [cls.get_or_insert(key, value = value) for key, value in settings.iteritems()]
        for item in new_settings:
            print item
            item.value = settings[item.key().name()]
        db.put(new_settings)


class StaticPage(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    content = db.TextProperty()

    tags = db.StringListProperty()
    is_published = db.BooleanProperty(default = False)
