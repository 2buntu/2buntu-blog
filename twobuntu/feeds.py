from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from twobuntu.accounts.models import Profile
from twobuntu.articles.models import Article
from twobuntu.categories.models import Category


class ArticleFeed(Feed):
    """
    Feed of articles.
    """

    def item_title(self, article):
        return article

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
    """
    Feed of most recent articles.
    """

    title = "Latest Articles on 2buntu"
    link = reverse_lazy('home')
    description = "Recently published articles about Ubuntu on the 2buntu blog."

    def items(self):
        return Article.objects.select_related('author', 'category').filter(status=Article.PUBLISHED)[:20]


class UserArticlesFeed(ArticleFeed):
    """
    Feed of articles written by a specific user.
    """

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


class CategoryArticlesFeed(ArticleFeed):
    """
    Feed of articles in a specific category.
    """

    def get_object(self, request, id):
        return get_object_or_404(Category, pk=id)

    def title(self, category):
        return 'Articles in %s' % category

    def link(self, category):
        return category.get_absolute_url()

    def description(self, category):
        return "Articles filed under %s." % category

    def items(self, category):
        return Article.objects.select_related('author', 'category').filter(status=Article.PUBLISHED, category=category)[:20]
