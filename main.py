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
import webapp2_extras.jinja2
from webapp2_extras import routes
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app

# importing apps
import views

import skollblog

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
#        'filters': {
#            'serve_image': shop.filters.serve_image,
#            'project_category': shop.filters.project_category,
#            },
#	 'globals': {
#	     'product_category_root': shop.filters.product_category_root,
#            'get_featured_products': shop.filters.get_featured_products,
#	     },
        },
    'template_path': os.path.join(os.path.dirname(__file__), 'templates/'),
    }   

#template.register_template_library('templatetags.site_info')

app = webapp2.WSGIApplication([
    # blog
    routes.PathPrefixRoute('/blog', skollblog.routes),
    #webapp2.Route(r'/blog/', handler=skollblog.views.BlogIndex, name='blog-index'),

    # portfolio


    # projects

    # index page
    webapp2.Route(r'/', handler=views.home, name='home'),

], debug=True, config=config)
	
def main():
	run_wsgi_app(app)

if __name__ == '__main__':
    main()
