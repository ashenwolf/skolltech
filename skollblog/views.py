#
from misc.decorators import render_to, BaseHandler 
from models import BlogPost, BlogCategory

class index(BaseHandler):
    @render_to("blog/index.html", 0)
    def get(self, category = None):
        cur_category = None
        categories = BlogCategory.all()

        if category:
            cur_category = BlogCategory.all().filter("slug =", category).get()
            posts = BlogPost.all().filter("category =", cur_category).order("-date_created")
        else:
            posts = BlogPost.all().order("-date_created")
            cur_category = None

        return {
            "section": "blog",
            "posts": posts,
            "cur_category": cur_category,
            "categories": categories,
        }

class post(BaseHandler):
    @render_to("blog/post.html", 0)
    def get(self, post_id):
        post = BlogPost.get_by_id(long(post_id))

        return {
            "section": "blog",
            "post": post,
        }
