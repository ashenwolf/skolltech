import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore

from skollimages.models import ImageRecord


class Technology(db.Model):
    name = db.StringProperty(required=True)
    image = blobstore.BlobReferenceProperty()

class ProjectCategory(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

class Project(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)

    image = db.ReferenceProperty(ImageRecord)
    teaser = db.TextProperty(required=True)
    
    description = db.TextProperty(Technology)

    category = db.ReferenceProperty(ProjectCategory)
    tags = db.StringListProperty()
    technologies = db.StringListProperty()

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

    url = db.LinkProperty()

    is_featured = db.BooleanProperty(default=False)

class HomeProject(Project):

    url = db.LinkProperty()
