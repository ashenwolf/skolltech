#
from webapp2 import Route

import views

routes = [
	# site settings
    Route(r'/', 					views.dashboard,			'admin-dashboard'),
    Route(r'/about/',               views.about,                'admin-about'),
    Route(r'/contacts/', 			views.contacts,				'admin-contacts'),

    # static pages
    Route(r'/staticpages/', 		views.staticpages_index,	'admin-staticpage-index'),
    Route(r'/satticpages/add/', 	views.staticpages_add,		'admin-staticpage-add'),
    Route(r'/satticpages/<page_id:\d+>/edit/', 	views.staticpages_edit,		'admin-staticpage-edit'),

    # delete item
    Route(r'/remove-entity/', 		views.remove,				'admin-remove-entity'),

    # authentication
    Route(r'/login/', 				views.login, 				'user-login'),
    Route(r'/logout/', 				views.logout,				'user-logout'),
]
