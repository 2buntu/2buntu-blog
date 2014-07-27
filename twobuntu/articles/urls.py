from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.articles.views',
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),

    url(r'^editor/(?:(?P<id>\d+)/)?$', 'editor', name='editor'),
    url(r'^(?P<action>submit|publish|release)/(?P<id>\d+)/$', 'modify', name='modify'),
    url(r'^schedule/(?P<id>\d+)/$', 'schedule', name='schedule'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='delete'),

    url(r'^search/$', 'search', name='search'),
    url(r'^markdown/$', 'markdown', name='markdown'),
)
