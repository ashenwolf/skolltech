import datetime
from google.appengine.ext import db

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
