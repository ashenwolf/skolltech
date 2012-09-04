#
from google.appengine.ext import db
from google.appengine.ext import blobstore

from misc.decorators import render_to, admin_required, login_required, BaseHandler 
from models import BlogPost, BlogCategory
from skollimages.models import ImageRecord
from forms import BlogPostForm, BlogCategoryForm

import webapp2
import json

class posts(BaseHandler):
    @login_required
    @render_to("admin/blog/posts.html", 0)
    def get(self):
        posts = BlogPost.all().order("-date_created")

        return {
            "admin_section": "admin-blog-posts",
            "posts": posts,
        }

class add(BaseHandler):
    @login_required
    @render_to("admin/blog/edit.html", 0)
    def get(self):
        form = BlogPostForm()

        return {
            "admin_section": "admin-blog-posts-new",
            "form": form,
        }

    @render_to("admin/blog/edit.html", 0)
    @login_required
    def post(self):
        form = BlogPostForm(self.request.POST)

        if form.validate():
            post = BlogPost(**form.data)
            post.save()
            self.redirect_to("admin-blog-post-edit-extra", post_id = post.key().id(), extra="saved")

        return {
            "admin_section": "admin-blog-posts-new",
            "form": form,
        }


class edit(BaseHandler):
    @login_required
    @render_to("admin/blog/edit.html", 0)
    def get(self, post_id, extra=""):
        post = BlogPost.get_by_id(long(post_id))
        form = BlogPostForm(obj = post)

        return {
            "admin_section": "admin-blog-posts",
            "form": form,
            "success": extra=="saved",
            "upload_url": blobstore.create_upload_url(webapp2.uri_for('image-upload')),
            "post": post,
        }

    @login_required
    @render_to("admin/blog/edit.html", 0)
    def post(self, post_id, extra=""):
        form = BlogPostForm(self.request.POST)
        success = False
        post = BlogPost.get_by_id(long(post_id))

        if form.validate():
            form.populate_obj(post)
            post.save()
            success = True

        return {
            "admin_section": "admin-blog-posts",
            "form": form,
            "success": success,
            "post": post,
        }

#lass delete(BaseHandler):
#    def post(self):
#        post = BlogPost.get_by_id(long(self.request.params.get("post_id", None)))
#        for blob in post.imagerecord_set: blob.image.delete()
#        db.delete(post.imagerecord_set)
#        post.delete()
#        self.response.headers['Content-Type'] = 'application/json'
#        self.response.out.write(json.dumps({"result": "ok"}))




class categories(BaseHandler):
    @admin_required
    @render_to("admin/blog/categories.html", 0)
    def get(self):
        categories = BlogCategory.all()

        return {
            "admin_section": "admin-blog-categories",
            "categories": categories,
        }

class categories_add(BaseHandler):
    @admin_required
    def post(self):
        form = BlogCategoryForm(self.request.POST)

        if form.validate():
            title = form.data["title"]
            slug = title.lower().replace(" ", "-")
            category = BlogCategory(title = title, slug = slug)
            category.put()

        self.redirect_to('admin-blog-categories')

class categories_edit(BaseHandler):
    @admin_required
    def post(self, category_id):
        form = BlogCategoryForm(self.request.POST)
        category = BlogCategory.get(long(category_id))

        if form.validate():
            slug = form.data["title"].lower().replace(" ", "-")
            form.populate_obj(category)
            category.put()

        return {
            "result": {
               "id": category.key().id(),
               "title": category.title,
               "slug": category.slug,
           }
        }
