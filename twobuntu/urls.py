from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from feeds import LatestArticlesFeed

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',          'twobuntu.views.index',    name='home'),
    url(r'^about/$',    'twobuntu.views.about',    name='about'),
    url(r'^links/$',    'twobuntu.views.links',    name='links'),
    url(r'^feedback/$', 'twobuntu.views.feedback', name='feedback'),

    url(r'^accounts/',   include('twobuntu.accounts.urls',   'accounts')),
    url(r'^articles/',   include('twobuntu.articles.urls',   'articles')),
    url(r'^api/',        include('twobuntu.api.urls',        'api')),
    url(r'^categories/', include('twobuntu.categories.urls', 'categories')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^rss/$', LatestArticlesFeed(), name='rss'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
