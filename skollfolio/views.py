from misc.decorators import render_to, BaseHandler 
from models import PortfolioProject, ProjectCategory

class index(BaseHandler):
    @render_to("projects/index.html", 0)
    def get(self, category = None):
        categories = ProjectCategory.all()
        if not category:
            projects = PortfolioProject.all().order("-date_created")
            cur_category = None
        else:
            cur_category = ProjectCategory.all().filter("slug =", category).get()
            projects = PortfolioProject.all().filter("category =", cur_category).order("-date_created")

        return {
            "section": "portfolio",
            "projects": projects,
            "cur_category": cur_category,
            "categories": categories,
        }

class project(BaseHandler):
    @render_to("projects/project.html", 0)
    def get(self, project_id):
        project = PortfolioProject.get_by_id(long(project_id))

        return {
            "section": "portfolio",
            "project": project,
        }
