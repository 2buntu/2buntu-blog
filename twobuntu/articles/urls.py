from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.articles.views',

    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),
    
    url(r'^editor/(?:(?P<id>\d+)/)?$', 'editor',  name='editor'),
    url(r'^publish/(?P<id>\d+)/$',     'publish', name='publish'),

    url(r'^search/$',   'search',   name='search'),
    url(r'^markdown/$', 'markdown', name='markdown'),
    
)
