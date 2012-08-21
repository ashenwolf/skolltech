#
from google.appengine.ext import db
from google.appengine.api import users
from misc.decorators import render_to, admin_required, BaseHandler 
from models import SiteSettings
from forms import SiteSettingsForm

class dashboard(BaseHandler):
    @admin_required
    @render_to("admin/dashboard.html", 0)
    def get(self):

        return {
            "admin_section": "admin-dashboard",
        }

class contacts(BaseHandler):
    @admin_required
    @render_to("admin/contacts.html", 0)
    def get(self):
        settings = dict([(setting.key().name(), setting.value) for setting in SiteSettings.all().fetch(None)])
        form = SiteSettingsForm(**settings)

        return {
            "admin_section": "admin-contacts",
            "form": form,
        }

    @admin_required
    @render_to("admin/contacts.html", 0)
    def post(self):
        form = SiteSettingsForm(self.request.POST)
        success = False

        if form.validate():
            SiteSettings.batch_set(form.data)
            success = True

        return {
            "admin_section": "admin-contacts",
            "success": success,
            "form": form,
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
