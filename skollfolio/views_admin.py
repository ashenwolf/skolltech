import webapp2
import json

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images

from misc.decorators import render_to, admin_required, login_required, BaseHandler 
from skollimages.models import ImageRecord

from models import PortfolioProject, ProjectCategory, Technology
from forms import PortfolioProjectForm, HomeProjectForm, ProjectCategoryForm, TechnologyForm

class portfolio(BaseHandler):
    @login_required
    @render_to("admin/projects/portfolio.html", 0)
    def get(self):
        projects = PortfolioProject.all().order("-date_created")

        return {
            "admin_section": "admin-projects-portfolio",
            "projects": projects,
        }


class add(BaseHandler):
    @login_required
    @render_to("admin/projects/edit.html", 0)
    def get(self):
        form = PortfolioProjectForm()
        form.technologies.choices = [(tech.key().id(), tech.title) for tech in Technology.all().fetch(None)]

        return {
            "admin_section": "admin-projects-new",
            "form": form,
        }

    @render_to("admin/projects/edit.html", 0)
    @login_required
    def post(self):
        form = PortfolioProjectForm(self.request.POST)
        form.technologies.choices = [(tech.key().id(), tech.title) for tech in Technology.all().fetch(None)]

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
        form.technologies.choices = [(tech.key().id(), tech.title) for tech in Technology.all().fetch(None)]

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
        form.technologies.choices = [(tech.key().id(), tech.title) for tech in Technology.all().fetch(None)]
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


#class delete(BaseHandler):
#    @login_required
#    def post(self):
#        project = PortfolioProject.get_by_id(long(self.request.params.get("project_id", None)))
#        for blob in project.imagerecord_set: blob.image.delete()
#        db.delete(project.imagerecord_set)
#        project.delete()
#        self.response.headers['Content-Type'] = 'application/json'
#        self.response.out.write(json.dumps({"result": "ok"}))

class categories(BaseHandler):
    @admin_required
    @render_to("admin/projects/categories.html", 0)
    def get(self):
        categories = ProjectCategory.all()

        return {
            "admin_section": "admin-projects-categories",
            "categories": categories,
        }


class categories_add(BaseHandler):
    @admin_required
    def post(self):
        form = ProjectCategoryForm(self.request.POST)

        if form.validate():
            title = form.data["title"]
            slug = title.lower().replace(" ", "-")
            category = ProjectCategory(title = title, slug = slug)
            category.put()

        self.redirect_to('admin-projects-categories')

class categories_edit(BaseHandler):
    @admin_required
    def post(self, category_id):
        form = ProjectCategoryForm(self.request.POST)

        if form.validate():
            slug = form.data["title"].lower().replace(" ", "-")
            category = ProjectCategory.get(long(category_id))
            form.populate_obj(category)
            category.put()

        return {
            "result": {
               "id": category.key().id(),
               "title": category.title,
               "slug": category.slug,
           }
        }





class technologies(BaseHandler):
    @admin_required
    @render_to("admin/projects/technologies.html", 0)
    def get(self):
        technologies = Technology.all()

        return {
            "admin_section": "admin-projects-technologies",
            "technologies": technologies,
        }


class technologies_add(BaseHandler):
    @admin_required
    def post(self):
        form = TechnologyForm(self.request.POST)

        if form.validate():
            title = form.data["title"]
            slug = title.strip().lower().replace(" ", "-")
            technology = Technology(title = title, slug = slug)
            technology.put()
        else:
            print form.errors

        self.redirect_to('admin-projects-technologies')

class technologies_edit(BaseHandler):
    @admin_required
    def post(self, technology_id):
        form = TechnologyForm(self.request.POST)

        if form.validate():
            slug = form.data["title"].strip().lower().replace(" ", "-")
            technology = Technology.get(long(category_id))
            form.populate_obj(technology)
            technology.put()

        return {
            "result": {
               "id": technology.key().id(),
               "title": technology.title,
               "slug": technology.slug,
           }
        }
