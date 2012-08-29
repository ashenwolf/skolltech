from misc.decorators import render_to, BaseHandler 
from models import PortfolioProject, ProjectCategory, Technology

class index(BaseHandler):
    @render_to("projects/index.html", 0)
    def get(self, category = None, technology = None):
        cur_technology = cur_category = None
        categories = ProjectCategory.all()

        if category:
            cur_category = ProjectCategory.all().filter("slug =", category).get()
            projects = PortfolioProject.all().filter("category =", cur_category).order("-date_created")
        elif technology:
            cur_technology = Technology.all().filter("slug =", technology).get()
            projects = PortfolioProject.all().filter("technologies =", cur_technology.key()).order("-date_created")
        else:
            projects = PortfolioProject.all().order("-date_created")
            cur_category = None

        return {
            "section": "portfolio",
            "projects": projects,
            "cur_category": cur_category,
            "cur_technology": cur_technology,
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
