#
from misc.decorators import render_to, BaseHandler 
from models import BlogPost

class index(BaseHandler):
    @render_to("blog/index.html", 0)
    def get(self):
        posts = BlogPost.all().order("-date_created")

        return {
            "section": "blog",
            "posts": posts,
        }

class post(BaseHandler):
    @render_to("blog/post.html", 0)
    def get(self, post_id):
        post = BlogPost.get_by_id(long(post_id))

        return {
            "section": "blog",
            "post": post,
        }
