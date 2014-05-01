from django.conf.urls import include, patterns, url

urlpatterns = patterns('twobuntu.api.views',

    url(r'^$', 'index', name='index'),

    url(r'^1.1/', include('twobuntu.api.v1_1.urls')),
    url(r'^1.2/', include('twobuntu.api.v1_2.urls')),
)
