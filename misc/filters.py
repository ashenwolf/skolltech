# -*- coding: utf-8 -*-
import webapp2

from jinja2 import nodes
from jinja2.ext import Extension

from google.appengine.api import images
#from google.appengine.api import memcache

default_cache_timeout = 7 * 24 * 3600 # 1 week

def serve_image(key, size, crop):
	if key:
		return images.get_serving_url(key, size, crop)
	else:
		return 'http://placehold.it/320x240'
