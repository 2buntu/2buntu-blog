from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.articles.views',

    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),

    url(r'^search/$', 'search', name='search'),
)
