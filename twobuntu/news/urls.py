from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.news.views',
    url(r'^add/$', 'add', name='add'),
)
