from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

from misc.decorators import render_to, admin_required, login_required, BaseHandler 

import webapp2
import json

from models import ImageRecord

class upload_url(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url(webapp2.uri_for('image-upload'))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('"' + upload_url + '"')


class upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]

        owner = self.request.params.get("owner", None)
        image = ImageRecord.for_key(owner, blob_info)
        image.save()

        result = {
            #"upload_url": blobstore.create_upload_url(webapp2.uri_for('image-upload')),
            "image_url" : images.get_serving_url(blob_info.key(), 240, False),
            "image_id"  : image.key().id(),
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))

class delete(BaseHandler):
    def post(self):
        record = ImageRecord.get_by_id(long(self.request.params.get("image_id", None)))
        record.image.delete()
        record.delete()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({"result": "ok"}))
