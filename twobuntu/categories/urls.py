from django.conf.urls import url

from twobuntu.categories import views
from twobuntu.feeds import CategoryArticlesFeed


urlpatterns = [
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', views.view, name='view'),
    url(r'^rss/(?P<id>\d+)/$', CategoryArticlesFeed(), name='rss'),
]
