from django.conf.urls import url

from twobuntu.touch import views


urlpatterns = [
    url(r'^device-art-generator/$', views.generator, name='generator'),
]
