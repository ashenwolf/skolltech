#
from webapp2 import Route

import views
import views_admin

routes = [
    Route('/', 								views.index,			'blog-index'),
    Route('/topic/<category:[a-z\-\.]+>/',  views.index,        	'blog-index-category'),
    Route('/<post_id:\d+>/', 				views.post, 			'blog-post'),
]

adminRoutes = [
    Route('/blog/posts/', 						views_admin.posts,		'admin-blog-posts'),
    Route('/blog/add/', 						views_admin.add,		'admin-blog-post-add'),
    Route('/blog/<post_id:\d+>/edit/', 			views_admin.edit, 		'admin-blog-post-edit'),
    Route('/blog/<post_id:\d+>/edit/?<extra:\w+>',   views_admin.edit, 	'admin-blog-post-edit-extra'),
#    Route('/blog/delete/', 						views_admin.delete, 	'admin-blog-post-delete'),

    Route('/blog/categories/', 					views_admin.categories, 'admin-blog-categories'),
    Route('/blog/categories/add/', 				views_admin.categories_add, 'admin-blog-categories-add'),
    Route('/blog/categories/<category_id:\d+>/edit/', 			views_admin.categories_edit, 'admin-blog-categories-edit'),
#    Route('/blog/categories/delete/', 			views_admin.categories_delete, 'admin-blog-categories-delete'),
]
