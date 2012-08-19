from webapp2 import Route

import views
import views_admin

routes = [
]

adminRoutes = [
    Route('/image/upload/', 					views_admin.upload,			'image-upload'),
    Route('/image/upload/url/', 				views_admin.upload_url,		'image-upload-url'),
    Route('/image/delete/', 					views_admin.delete,			'image-delete'),
#    Route('/blog/<post_id:\d+>/edit/', 			views_admin.edit, 		'admin-blog-post-edit'),
]
