import datetime
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore

ImageKinds = ["gallery", "front", "sketch"]

class ImageRecord(db.Model):
    image = blobstore.BlobReferenceProperty(required = True)
    owner = db.ReferenceProperty(required = True)
    image_type = db.StringProperty(default = "gallery")

    title = db.StringProperty()
    description = db.StringProperty()

    @classmethod
    def for_key(cls, owner, blob, image_type = "gallery"):
    	owner_model, owner_id = owner.split(":")
    	key = db.Key.from_path(owner_model, long(owner_id))
    	record = ImageRecord(owner = key, image = blob, image_type = image_type)
    	return record
