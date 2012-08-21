from misc.decorators import render_to, BaseHandler 
from skollfolio.models import PortfolioProject
from skollblog.models import BlogPost

class home(BaseHandler):
    @render_to("index.html", 0)
    def get(self):
        featured = PortfolioProject.all().filter("is_featured =", True).fetch(None)
        projects = PortfolioProject.all().order("-date_created").fetch(4)
        posts = BlogPost.all().order("-date_created").fetch(2)

        return {
            "featured": featured,
            "projects": projects,
            "posts": posts,
        }


errors = {
    "forbidden": {
        "title": "Access forbidden",
        "text": "Looks like you don't have enough rights to access this area. Please contact site administrator."
    }
}

class error(BaseHandler):
    @render_to("error.html", 0)
    def get(self, error_id):
        return {
            "title": errors[error_id]["title"],
            "text": errors[error_id]["text"],
        }
