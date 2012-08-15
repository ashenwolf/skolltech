import os
import webapp2

from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.api import memcache

default_cache_timeout = 3 * 24 * 3600 # 1 day

class BaseHandler(webapp2.RequestHandler):
	@webapp2.cached_property
	def jinja2(self):
		# Returns a Jinja2 renderer cached in the app registry.
		return jinja2.get_jinja2(app=self.app)
		
	def render_response(self, _template, **context):
		# Renders a template and writes the result to the response.
		context['user'] = users.get_current_user()
		context['is_admin'] = users.is_current_user_admin()
		rv = self.jinja2.render_template(_template, **context)
		self.response.write(rv)

	def render_response_cache(self, key, cache_timeout, template, **context):
		# Renders a template and writes the result to the response.
		context['user'] = users.get_current_user()
		context['is_admin'] = users.is_current_user_admin()
		key = key + ("_admin" if context['is_admin'] else "_user")
		
		page = memcache.get(key)
		if page:
			self.response.write(page)
		else:
			rv = self.jinja2.render_template(template, **context)
			memcache.add(key, rv, cache_timeout)
			self.response.write(rv)

def render_to(template_path, cache_timeout = default_cache_timeout):
	def renderer(func):
		def wrapper(self, *args, **kw):
			output = func(self, *args, **kw)
			if isinstance(output, dict):
				if cache_timeout > 0:
					self.render_response_cache(self.request.path_qs, cache_timeout, template_path, **output)
				else:
					self.render_response(template_path, **output)
				return
			return output
		return wrapper
	return renderer


def admin_required(func):
	def wrapper(self, *args, **kw):
		if users.is_current_user_admin():
			return func(self, *args, **kw)
		else:
			return self.redirect(users.create_login_url(self.request.uri))
	return wrapper
