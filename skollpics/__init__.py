from webapp2 import Route

import views
#import views_admin

routes = [
]

adminRoutes = [
    Route('/image/upload/', 					views.upload,			'image-upload'),
#    Route('/blog/<post_id:\d+>/edit/', 			views_admin.edit, 		'admin-blog-post-edit'),
]
