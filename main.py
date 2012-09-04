#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
import jinja2
#import webapp2_extras.jinja2
from webapp2_extras import routes
#from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app

# importing apps
import views
import misc.filters

import skolladmin
import skollblog
import skollfolio
import skollimages

class NullUndefined(jinja2.Undefined):
    def __int__(self):
        return ''
    def __float__(self):
        return ''
    def __getattr__(self, name):
        return ''

config = {
    'webapp2_extras.i18n': {
        'translations_path': os.path.join(os.path.dirname(__file__), 'locale'),
        },
    'webapp2_extras.jinja2' : {
        'environment_args': {
            'extensions': ['jinja2.ext.i18n', 'jinja2.ext.autoescape', 'jinja2.ext.with_'],
            'undefined': NullUndefined,
            },
        'filters': {
            'serve_image': misc.filters.serve_image,
            'upload_url': misc.filters.upload_url,
            'htmlify': misc.filters.htmlify,
            },
	    'globals': {
            'url': webapp2.uri_for,
            'settings': skolladmin.models.SiteSettings,
	        },
        },
    'template_path': os.path.join(os.path.dirname(__file__), 'templates/'),
    }   

#template.register_template_library('templatetags.site_info')

app = webapp2.WSGIApplication([
    # blog
    routes.PathPrefixRoute('/blog', skollblog.routes),

    # portfolio
    routes.PathPrefixRoute('/portfolio', skollfolio.routes),

    # projects
    #routes.PathPrefixRoute('/projects', skollprojects.routes),


    # admin routes
    routes.PathPrefixRoute('/manage', skolladmin.routes),
    routes.PathPrefixRoute('/manage', skollblog.adminRoutes),
    routes.PathPrefixRoute('/manage', skollfolio.adminRoutes),

    # image management
    routes.PathPrefixRoute('/manage', skollimages.adminRoutes),

    # index page
    webapp2.Route(r'/', handler=views.home, name='home'),
    webapp2.Route(r'/<page_slug:[a-z\-\.\z]+>/', handler=views.staticpage, name="staticpage"),
    webapp2.Route(r'/error/<error_id:\w+>', handler=views.error, name='error'),

], debug=True, config=config)
	
def main():
	run_wsgi_app(app)

if __name__ == '__main__':
    main()
