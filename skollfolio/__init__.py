#
from webapp2 import Route

import views
import views_admin

routes = [
#    Route('/', 							views.index,		'portfolio-index'),
#    Route('/<article_id:\d+>/', 		views.project, 		'portfolio-project'),
#    Route('/add/', 						views.add,			'portfolio-article-add'),
#    Route('/<article_id:\d+>/edit/', 	views.edit, 		'portfolio-article-edit'),
#    Route('/<article_id:\d+>/edit/', 	views.remove, 		'portfolio-article-remove'),
]

adminRoutes = [
    Route('/projects/portfolio/', 				views_admin.portfolio, 		'admin-projects-portfolio'),
    Route('/projects/add/', 					views_admin.add, 			'admin-projects-add'),
    Route('/projects/<project_id:\d+>/edit/', 	views_admin.edit, 			'admin-projects-edit'),
    Route('/projects/<project_id:\d+>/edit/?<extra:\w+>',   views_admin.edit, 	'admin-projects-edit-extra'),
    Route('/projects/set-teaser/', 				views_admin.set_teaser,		'admin-projects-set-teaser'),
    Route('/projects/delete/', 					views_admin.delete,			'admin-projects-delete'),
    Route('/projects/categories/', 				views_admin.categories,		'admin-projects-categories'),
]
