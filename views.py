from misc.decorators import render_to, BaseHandler 
from skollfolio.models import PortfolioProject

class home(BaseHandler):
    @render_to("index.html", 0)
    def get(self):
        projects = PortfolioProject.all().fetch(None)
        return {
            "projects": projects,
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
