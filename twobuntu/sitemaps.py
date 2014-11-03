from django.contrib import sitemaps
from django.core.urlresolvers import reverse


class HomePageSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'yearly'

    def items(self):
        return ['about', 'links', 'feedback', 'join']

    def location(self, item):
        return reverse(item)
