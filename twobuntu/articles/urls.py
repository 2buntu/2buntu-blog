from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.articles.views',

    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),

    url(r'^editor/(?:(?P<id>\d+)/)?$', 'editor',   name='editor'),
    url(r'^submit/(?P<id>\d+)/$',      'submit',   name='submit'),
    url(r'^publish/(?P<id>\d+)/$',     'publish',  name='publish'),
    url(r'^release/(?P<id>\d+)/$',     'release',  name='release'),
    url(r'^schedule/(?P<id>\d+)/$',    'schedule', name='schedule'),

    url(r'^search/$',   'search',   name='search'),
    url(r'^markdown/$', 'markdown', name='markdown'),

)
