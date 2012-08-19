#
from webapp2 import Route

import views
import views_admin

routes = [
    Route('/', 							views.index,			'blog-index'),
    Route('/<post_id:\d+>/', 			views.post, 			'blog-post'),
]

adminRoutes = [
    Route('/blog/posts/', 						views_admin.posts,		'admin-blog-posts'),
    Route('/blog/add/', 						views_admin.add,		'admin-blog-post-add'),
    Route('/blog/<post_id:\d+>/edit/', 			views_admin.edit, 		'admin-blog-post-edit'),
    Route('/blog/<post_id:\d+>/edit/?<extra:\w+>',   views_admin.edit, 		'admin-blog-post-edit-extra'),
    Route('/blog/<post_id:\d+>/remove/', 		views_admin.remove, 	'admin-blog-post-remove'),
    Route('/blog/categories/', 					views_admin.categories, 'admin-blog-categories'),
]
