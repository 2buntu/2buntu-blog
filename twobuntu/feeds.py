from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from twobuntu.accounts.models import Profile
from twobuntu.articles.models import Article

class ArticleFeed(Feed):
    """Feed of articles."""

    def item_title(self, article):
        return article.title

    def item_link(self, article):
        return article.get_absolute_url()

    def item_description(self, article):
        return article.render()

    def item_author_name(self, article):
        return article.author.profile

    def item_author_link(self, article):
        return article.author.profile.get_absolute_url()

    def item_pubdate(self, article):
        return article.date

class LatestArticlesFeed(ArticleFeed):
    """Feed of most recent articles."""

    title = "Latest Articles on 2buntu"
    link = reverse_lazy('home')
    description = "Recently published articles about Ubuntu on the 2buntu blog."

    def items(self):
        return Article.objects.select_related('author', 'category').filter(status=Article.PUBLISHED)[:20]

class UserArticlesFeed(ArticleFeed):
    """Feed of articles written by a specific user."""

    def get_object(self, request, id):
        return get_object_or_404(Profile, pk=id)

    def title(self, profile):
        return 'Articles by %s' % profile

    def link(self, profile):
        return profile.get_absolute_url()

    def description(self, profile):
        return "Recently published articles written by %s." % profile

    def items(self, profile):
        return Article.objects.select_related('author', 'category').filter(status=Article.PUBLISHED, author=profile.user)[:20]
