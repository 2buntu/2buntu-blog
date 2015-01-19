from django.conf.urls import include, patterns, url

urlpatterns = patterns('',
    # Version 1.2 is the current version
    url(r'^$', 'twobuntu.api.v1_2.views.index', name='index'),
    url(r'^1.2/', include('twobuntu.api.v1_2.urls', '1.2')),
)
