#
from webapp2 import Route

import views

routes = [
    Route(r'/', 			views.BlogList,			'blog-list'),
    Route(r'/<article_id:\d+>/', 	views.BlogArticle, 		'blog-article'),
    Route(r'/add/', 			views.BlogArticleAdd,		'blog-article-add'),
    Route(r'/<article_id:\d+>/edit/', 	views.BlogArticleEdit, 		'blog-article-edit'),
    Route(r'/<article_id:\d+>/edit/', 	views.BlogArticleRemove, 	'blog-article-remove'),
]
