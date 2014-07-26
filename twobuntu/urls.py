from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from twobuntu.feeds import LatestArticlesFeed

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'twobuntu.views.index', name='home'),
    url(r'^about/$', 'twobuntu.views.about', name='about'),
    url(r'^links/$', 'twobuntu.views.links', name='links'),
    url(r'^feedback/$', 'twobuntu.views.feedback', name='feedback'),
    url(r'^join/$', 'twobuntu.views.join', name='join'),
    url(r'^opensearch.xml$', 'twobuntu.views.opensearch', name='opensearch'),

    url(r'^accounts/', include('twobuntu.accounts.urls', 'accounts')),
    url(r'^ads/', include('twobuntu.ads.urls', 'ads')),
    url(r'^articles/', include('twobuntu.articles.urls', 'articles')),
    url(r'^api/', include('twobuntu.api.urls', 'api')),
    url(r'^categories/', include('twobuntu.categories.urls', 'categories')),
    url(r'^images/', include('twobuntu.images.urls', 'images')),
    url(r'^news/', include('twobuntu.news.urls', 'news')),

    # Shortened URLs can redirect anywhere
    url(r'^(?P<key>[0-9a-f]{6})/$', 'twobuntu.shorturls.views.shorturl'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rss/$', LatestArticlesFeed(), name='rss'),

    # Catch requests to the old URLs for a while with a permanent 301 redirect
    url(r'^(?P<id>\d+)/', 'twobuntu.views.old'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
