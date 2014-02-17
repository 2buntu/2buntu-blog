from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.categories.views',

    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', 'view', name='view'),
)
