from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.images.views',

    url(r'^upload/$', 'upload', name='upload'),
)
