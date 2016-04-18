from django.conf.urls import url

from twobuntu.news import views


urlpatterns = [
    url(r'^add/$', views.add, name='add'),
]
