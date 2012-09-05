import webapp2
import json
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import users
from misc.decorators import render_to, admin_required, BaseHandler 
from models import SiteSettings, StaticPage
from forms import SiteSettingsForm, SiteContactsForm, StaticPageForm

class dashboard(BaseHandler):
    @admin_required
    @render_to("admin/dashboard.html", 0)
    def get(self):

        return {
            "admin_section": "admin-dashboard",
        }

class about(BaseHandler):
    @admin_required
    @render_to("admin/about.html", 0)
    def get(self):
        settings = dict([(setting.key().name(), setting.value) for setting in SiteSettings.all().fetch(None)])
        form = SiteSettingsForm(**settings)

        return {
            "admin_section": "admin-about",
            "form": form,
        }

    @admin_required
    @render_to("admin/about.html", 0)
    def post(self):
        form = SiteSettingsForm(self.request.POST)
        success = False

        if form.validate():
            SiteSettings.batch_set(form.data)
            success = True

        return {
            "admin_section": "admin-about",
            "success": success,
            "form": form,
        }

class contacts(BaseHandler):
    @admin_required
    @render_to("admin/contacts.html", 0)
    def get(self):
        settings = dict([(setting.key().name(), setting.value) for setting in SiteSettings.all().fetch(None)])
        form = SiteContactsForm(**settings)

        return {
            "admin_section": "admin-contacts",
            "form": form,
        }

    @admin_required
    @render_to("admin/contacts.html", 0)
    def post(self):
        form = SiteContactsForm(self.request.POST)
        success = False

        if form.validate():
            SiteSettings.batch_set(form.data)
            success = True

        return {
            "admin_section": "admin-contacts",
            "success": success,
            "form": form,
        }

class staticpages_index(BaseHandler):
    @admin_required
    @render_to("admin/staticpages/index.html", 0)
    def get(self):
        pages = StaticPage.all()

        return {
            "admin_section": "admin-staticpages",
            "pages": pages,
        }

class staticpages_add(BaseHandler):
    @admin_required
    @render_to("admin/staticpages/edit.html", 0)
    def get(self):
        form = StaticPageForm()

        return {
            "admin_section": "admin-staticpage-add",
            "form": form,
        }

    @admin_required
    @render_to("admin/staticpages/edit.html", 0)
    def post(self):
        form = StaticPageForm(self.request.POST)

        if form.validate():
            page = StaticPage(**form.data)
            page.save()
            self.redirect_to("admin-staticpage-edit", page_id = page.key().id())

        return {
            "admin_section": "admin-staticpage-add",
            "form": form,
        }

class staticpages_edit(BaseHandler):
    @admin_required
    @render_to("admin/staticpages/edit.html", 0)
    def get(self, page_id, extra = None):
        page = StaticPage.get_by_id(long(page_id))
        form = StaticPageForm(obj = page)

        return {
            "admin_section": "admin-staticpage-edit",
            "form": form,
            "success": extra=="saved",
            "upload_url": blobstore.create_upload_url(webapp2.uri_for('image-upload')),
            "page": page,
        }

    @admin_required
    @render_to("admin/staticpages/edit.html", 0)
    def post(self, page_id):
        page = StaticPage.get_by_id(long(page_id))
        form = StaticPageForm(self.request.POST)
        success = False

        if form.validate():
            form.populate_obj(page)
            page.save()
            success = True

        return {
            "admin_section": "admin-staticpage-edit",
            "form": form,
            "success": success,
            "page": page,
        }

class login(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class logout(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url(self.request.uri))
        else:
            self.redirect("/")

class remove(BaseHandler):
    def post(self):
        item = db.get(db.Key.from_path(self.request.params.get("item_type", None), long(self.request.params.get("item_id", None))))
        for blob in item.imagerecord_set: blob.image.delete()
        db.delete(item.imagerecord_set)
        item.delete()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({"result": "ok"}))
