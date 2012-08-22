import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore


class BlogCategory(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    order = db.IntegerProperty(required=True, default=1)

    def __unicode__(self):
        return self.title


class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    #image = blobstore.BlobReferenceProperty()
    teaser = db.StringProperty()
    content = db.TextProperty(required=True)

    category = db.ReferenceProperty(BlogCategory)
    tags = db.StringListProperty()

    date_created = db.DateTimeProperty(required=True, auto_now_add=True)
    #date_published = db.DateTimeProperty()
    is_published = db.BooleanProperty(required=True, default=True)

    author = db.UserProperty(required=True, auto_current_user_add=True) 

    #role = db.StringProperty(required=True, choices=set(["executive", "manager", "producer"]))
