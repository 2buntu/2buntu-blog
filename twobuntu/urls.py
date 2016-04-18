from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from twobuntu import views
from twobuntu.feeds import LatestArticlesFeed
from twobuntu.sitemaps import HomePageSitemap, StaticViewSitemap


sitemaps = {
    'home': HomePageSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^links/$', views.links, name='links'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^join/$', views.join, name='join'),
    url(r'^opensearch\.xml$', views.opensearch, name='opensearch'),

    url(r'^accounts/', include('twobuntu.accounts.urls', 'accounts')),
    url(r'^articles/', include('twobuntu.articles.urls', 'articles')),
    url(r'^api/', include('twobuntu.api.urls', 'api')),
    url(r'^categories/', include('twobuntu.categories.urls', 'categories')),
    url(r'^images/', include('twobuntu.images.urls', 'images')),
    url(r'^news/', include('twobuntu.news.urls', 'news')),
    url(r'^touch/', include('twobuntu.touch.urls', 'touch')),

    # Shortened URLs can redirect anywhere
    url(r'^(?P<key>[0-9a-f]{6})/', include('twobuntu.shorturls.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rss/$', LatestArticlesFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
