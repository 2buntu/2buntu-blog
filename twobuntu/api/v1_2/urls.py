from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.api.v1_2.views',
    url(r'^articles/$', 'articles', name='articles'),
    url(r'^articles/(?P<id>\d+)/$', 'article_by_id', name='article_by_id'),

    url(r'^authors/$', 'authors', name='authors'),
    url(r'^authors/(?P<id>\d+)/$', 'author_by_id', name='author_by_id'),
    url(r'^authors/(?P<id>\d+)/articles/$', 'articles_by_author', name='articles_by_author'),

    url(r'^categories/$', 'categories', name='categories'),
    url(r'^categories/(?P<id>\d+)/articles/$', 'articles_by_category', name='articles_by_category'),
)
