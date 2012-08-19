#
from google.appengine.ext import db
from misc.decorators import render_to, admin_required, login_required, BaseHandler 
from models import BlogPost
from forms import BlogPostForm

class posts(BaseHandler):
    @login_required
    @render_to("admin/blog/posts.html", 0)
    def get(self):
        posts = BlogPost.all().order("-date_created")

        return {
            "admin_section": "admin-blog-posts",
            "posts": posts,
        }


class categories(BaseHandler):
    @admin_required
    @render_to("admin/blog/categories.html", 0)
    def get(self):
        posts = BlogPost.all().order("-date_created")

        return {
            "admin_section": "admin-blog-categories",
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
        }

    @login_required
    @render_to("admin/blog/edit.html", 0)
    def post(self, post_id, extra=""):
        post = BlogPost.get_by_id(long(post_id))
        form = BlogPostForm(self.request.POST)

        if form.validate():
            form.populate_obj(post)
            post.save()
            success = True

        return {
            "admin_section": "admin-blog-posts",
            "form": form,
            "success": success or None
        }

class remove(BaseHandler):
    pass

