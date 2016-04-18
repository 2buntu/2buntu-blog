from django.conf.urls import url

from twobuntu.accounts import views
from twobuntu.feeds import UserArticlesFeed


urlpatterns = [
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', views.profile, name='profile'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^register/$', views.register, name='register'),
    url(r'^register/confirm/(?P<key>[0-9a-f]{32})/$', views.register_confirm, name='register_confirm'),

    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset/confirm/(?P<key>[0-9a-f]{32})/$', views.reset_confirm, name='reset_confirm'),

    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
    url(r'^rss/(?P<id>\d+)/$', UserArticlesFeed(), name='rss'),
]
