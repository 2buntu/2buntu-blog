from django.conf.urls import url

from twobuntu.images import views


urlpatterns = [
    url(r'^view/(?P<id>\d+)/$', views.view, name='view'),
    url(r'^upload/$', views.upload, name='upload'),
]
