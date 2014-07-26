from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.api.v1_1.views',
    url(r'^articles/published/$', 'published'),
    url(r'^articles/modified/$', 'modified'),
    url(r'^articles/(?P<id>\d+)/$', 'article'),
)
