from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.images.views',
    url(r'^view/(?P<id>\d+)/$', 'view', name='view'),
    url(r'^upload/$', 'upload', name='upload'),
)
