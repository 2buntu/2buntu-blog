from django.conf.urls import patterns, url

from twobuntu.feeds import UserArticlesFeed

urlpatterns = patterns('twobuntu.accounts.views',
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'profile', name='profile'),

    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    url(r'^register/$', 'register', name='register'),
    url(r'^register/confirm/(?P<key>[0-9a-f]{32})/$', 'register_confirm', name='register_confirm'),

    url(r'^reset/$', 'reset', name='reset'),
    url(r'^reset/confirm/(?P<key>[0-9a-f]{32})/$', 'reset_confirm', name='reset_confirm'),

    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit'),
    url(r'^rss/(?P<id>\d+)/$', UserArticlesFeed(), name='rss'),
)
