#
from google.appengine.ext import db
from google.appengine.api import users
from misc.decorators import render_to, admin_required, BaseHandler 

class dashboard(BaseHandler):
    @admin_required
    @render_to("admin/dashboard.html", 0)
    def get(self):

        return {
            "admin_section": "admin-dashboard",
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
