from django.conf.urls import url

from twobuntu.articles import views


urlpatterns = [
    url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', views.view, name='view'),

    url(r'^editor/(?:(?P<id>\d+)/)?$', views.editor, name='editor'),
    url(r'^(?P<action>submit|publish|release)/(?P<id>\d+)/$', views.modify, name='modify'),
    url(r'^schedule/(?P<id>\d+)/$', views.schedule, name='schedule'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),

    url(r'^search/$', views.search, name='search'),
    url(r'^markdown/$', views.markdown, name='markdown'),
]
