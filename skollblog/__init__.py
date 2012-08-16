#
from webapp2 import Route

import views

routes = [
    Route('/', 							views.BlogIndex,			'blog-index'),
    Route('/<article_id:\d+>/', 		views.BlogArticle, 			'blog-article'),
    Route('/add/', 						views.BlogArticleAdd,		'blog-article-add'),
    Route('/<article_id:\d+>/edit/', 	views.BlogArticleEdit, 		'blog-article-edit'),
    Route('/<article_id:\d+>/edit/', 	views.BlogArticleRemove, 	'blog-article-remove'),
]
