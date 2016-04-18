from django.conf.urls import url

from twobuntu.shorturls import views


urlpatterns = [
    url(r'^$', views.shorturl),
]
