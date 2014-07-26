from django.conf.urls import patterns, url

from twobuntu.feeds import CategoryArticlesFeed

urlpatterns = patterns('twobuntu.categories.views',
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),
    url(r'^rss/(?P<id>\d+)/$', CategoryArticlesFeed(), name='rss'),
)
