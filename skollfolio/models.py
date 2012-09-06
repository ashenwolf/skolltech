import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore

from skollimages.models import ImageRecord


class Technology(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    image_small = blobstore.BlobReferenceProperty()
    image_large = blobstore.BlobReferenceProperty()

    def __unicode__(self):
        return self.title

class ProjectCategory(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    order = db.IntegerProperty(required=True, default=1)

    def __unicode__(self):
        return self.title

class Project(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    image = db.ReferenceProperty(ImageRecord)
    teaser = db.TextProperty(required=True)
    
    description = db.TextProperty(Technology)

    category = db.ReferenceProperty(ProjectCategory)
    tags = db.StringListProperty()
    technologies = db.ListProperty(db.Key)
    date_created = db.DateTimeProperty(required=True, auto_now_add=True)
    is_published = db.BooleanProperty(required=True, default=True)


    author = db.UserProperty(required=True, auto_current_user_add=True)

    def teaser_image(self):
        result = None
        try:
            result = self.image.image
        except db.ReferencePropertyResolveError:
            self.image = None
            self.save()
        except:
            pass
        return result

class PortfolioProject(Project):
    problem = db.TextProperty()
    solution = db.TextProperty()
    customer = db.TextProperty()

    team = db.TextProperty()

    url = db.LinkProperty()

    is_featured = db.BooleanProperty(default=False)

class HomeProject(Project):

    url = db.LinkProperty()
