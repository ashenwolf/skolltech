import webapp2
import json

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images

from misc.decorators import render_to, admin_required, login_required, BaseHandler 
from skollimages.models import ImageRecord

from models import PortfolioProject
from forms import PortfolioProjectForm, HomeProjectForm

class portfolio(BaseHandler):
    @login_required
    @render_to("admin/projects/portfolio.html", 0)
    def get(self):
        projects = PortfolioProject.all().order("-date_created")

        return {
            "admin_section": "admin-projects-portfolio",
            "projects": projects,
        }


class categories(BaseHandler):
    @admin_required
    @render_to("admin/projects/categories.html", 0)
    def get(self):
        categories = ProjectCategory.all()

        return {
            "admin_section": "admin-projects-categories",
            "categories": categories,
        }

class add(BaseHandler):
    @login_required
    @render_to("admin/projects/edit.html", 0)
    def get(self):
        form = PortfolioProjectForm()

        return {
            "admin_section": "admin-projects-new",
            "form": form,
        }

    @render_to("admin/projects/edit.html", 0)
    @login_required
    def post(self):
        form = PortfolioProjectForm(self.request.POST)

        if form.validate():
            project = PortfolioProject(**form.data)
            project.save()
            self.redirect_to("admin-projects-edit-extra", project_id = project.key().id(), extra="saved")

        return {
            "admin_section": "admin-projects-new",
            "form": form,
        }


class edit(BaseHandler):
    @login_required
    @render_to("admin/projects/edit.html", 0)
    def get(self, project_id, extra=""):
        project = PortfolioProject.get_by_id(long(project_id))
        form = PortfolioProjectForm(obj = project)

        return {
            "admin_section": "admin-projects-portfolio",
            "form": form,
            "success": extra == "saved",
            "upload_url": blobstore.create_upload_url(webapp2.uri_for('image-upload')),
            "project": project,
        }

    @login_required
    @render_to("admin/projects/edit.html", 0)
    def post(self, project_id, extra=""):
        project = PortfolioProject.get_by_id(long(project_id))
        form = PortfolioProjectForm(self.request.POST)
        success = False

        if form.validate():
            form.populate_obj(project)
            project.save()
            success = True

        return {
            "admin_section": "admin-projects-portfolio",
            "form": form,
            "success": success,
            "project": project,
        }

class set_teaser(BaseHandler):
    @login_required
    def post(self):
        project = PortfolioProject.get_by_id(long(self.request.params.get("project_id", None)))
        teaser = ImageRecord.get_by_id(long(self.request.params.get("teaser_id", None)))
        project.image = teaser
        project.save()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({
            "teaser": images.get_serving_url(teaser.image.key(), 800, False)
            }))


class delete(BaseHandler):
    @login_required
    def post(self):
        project = PortfolioProject.get_by_id(long(self.request.params.get("project_id", None)))
        for blob in project.imagerecord_set: blob.image.delete()
        db.delete(project.imagerecord_set)
        project.delete()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({"result": "ok"}))
