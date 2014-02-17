from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.accounts.views',

    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'profile', name='profile'),

    url(r'^login/$',  'login',  name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    url(r'^register/$',                      'register', name='register'),
    url(r'^confirm/(?P<key>[0-9a-f]{32})/$', 'confirm',  name='confirm'),
)
