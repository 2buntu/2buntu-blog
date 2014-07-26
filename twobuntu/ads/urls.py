from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.ads.views',
    url(r'^$', 'index', name='index'),
)
