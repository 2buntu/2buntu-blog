from django.conf.urls import patterns, url

urlpatterns = patterns('twobuntu.touch.views',
    url(r'^device-art-generator/$', 'generator', name='generator'),
)
