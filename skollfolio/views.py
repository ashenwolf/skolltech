from misc.decorators import render_to, BaseHandler 
from models import PortfolioProject

class index(BaseHandler):
    @render_to("projects/index.html", 0)
    def get(self):
        projects = PortfolioProject.all().order("-date_created")

        return {
            "section": "portfolio",
            "projects": projects,
        }

class project(BaseHandler):
    @render_to("projects/item.html", 0)
    def get(self, project_id):
        project = PortfolioProject.get_by_id(long(project_id))

        return {
            "section": "portfolio",
            "project": project,
        }
