from django.conf.urls import url

from twobuntu.api.v1_2 import views


urlpatterns = [
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^articles/(?P<id>\d+)/$', views.article_by_id, name='article_by_id'),

    url(r'^authors/$', views.authors, name='authors'),
    url(r'^authors/(?P<id>\d+)/$', views.author_by_id, name='author_by_id'),
    url(r'^authors/(?P<id>\d+)/articles/$', views.articles_by_author, name='articles_by_author'),

    url(r'^categories/$', views.categories, name='categories'),
    url(r'^categories/(?P<id>\d+)/articles/$', views.articles_by_category, name='articles_by_category'),
]
