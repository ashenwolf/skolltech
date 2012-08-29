from misc.decorators import render_to, BaseHandler 
from skollfolio.models import PortfolioProject, Technology
from skollblog.models import BlogPost
from skolladmin.models import StaticPage

class home(BaseHandler):
    @render_to("index.html", 0)
    def get(self):
        featured = PortfolioProject.all().filter("is_featured =", True).fetch(None)
        projects = PortfolioProject.all().order("-date_created").fetch(4)
        technologies = Technology.all().fetch(None)
        posts = BlogPost.all().order("-date_created").fetch(2)

        return {
            "featured": featured,
            "projects": projects,
            "technologies": technologies,
            "posts": posts,
        }


errors = {
    403: {
        "title": "Error 403. Access forbidden",
        "text": "<br />Looks like you don't have enough rights to access this area. Please contact site administrator.<br /><br /><br /><br /><br />"
    },
    404: {
        "title": "Error 404. Page not found",
        "text": "<br />The page you have requested could not be found. Please check the url and try again.<br /><br /><br /><br /><br />"
    },
}

class staticpage(BaseHandler):
    @render_to("page.html", 0)
    def get(self, page_slug):
        page = StaticPage.all().filter("slug =", page_slug.lower()).get()
        if not page:
            self.redirect_to('error', error_id = 404)

        return {
            "section": page_slug,
            "page": page,
        }

class error(BaseHandler):
    @render_to("error.html", 0)
    def get(self, error_id):
        return {
            "title": errors[int(error_id)]["title"],
            "text": errors[int(error_id)]["text"],
        }
