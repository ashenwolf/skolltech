#
from google.appengine.ext import db
from decorators import render_to, BaseHandler 
from models import BlogPost
from forms import BlogPostForm

class BlogIndex(BaseHandler):
    @render_to("blog/index.html", 0)
    def get(self):
        posts = BlogPost.all().order("-date_created")

        return {
            "section": "blog",
            "posts": posts,
        }

class BlogArticle(BaseHandler):
    @render_to("blog/article.html", 0)
    def get(self, article_id):
        post = BlogPost.get_by_id(long(article_id))

        return {
            "section": "blog",
            "post": post,
        }

class BlogArticleAdd(BaseHandler):
    @render_to("blog/edit.html", 0)
    def get(self):
        form = BlogPostForm()

        return {
            "section": "blog",
            "form": form,
        }

    @render_to("blog/edit.html", 0)
    def post(self):
        form = BlogPostForm(self.request.POST)

        if form.validate():
            post = BlogPost(**form.data)
            post.save()
            self.redirect_to("blog-article", article_id = post.key().id())

        return {
            "section": "blog",
            "form": form,
        }


class BlogArticleEdit(BaseHandler):
    @render_to("blog/edit.html", 0)
    def get(self, article_id):
        post = BlogPost.get_by_id(long(article_id))
        form = BlogPostForm(obj = post)

        return {
            "section": "blog",
            "form": form,
        }

    @render_to("blog/edit.html", 0)
    def post(self, article_id):
        post = BlogPost.get_by_id(long(article_id))
        form = BlogPostForm(self.request.POST)

        if form.validate():
            form.populate_obj(post)
            post.save()
            self.redirect_to("blog-article", article_id = post.key().id())

        return {
            "section": "blog",
            "form": form,
        }

class BlogArticleRemove(BaseHandler):
    pass
