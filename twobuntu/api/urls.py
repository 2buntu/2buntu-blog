from django.conf.urls import include, url

from twobuntu.api.v1_2 import views


urlpatterns = [
    # Version 1.2 is the current version
    url(r'^$', views.index, name='index'),
    url(r'^1.2/', include('twobuntu.api.v1_2.urls', '1.2')),
]
