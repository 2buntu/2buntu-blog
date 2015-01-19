from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory

from twobuntu.articles.models import Article
from twobuntu.articles.views import view as view_article
from twobuntu.utils import dummy_article, dummy_category, dummy_user


class TestArticlePermission(TestCase):
    """
    Test that the correct users have access to the correct articles.
    """

    def setUp(self):
        # Create the request factory
        self.factory = RequestFactory()
        # Create three users - two normal users and an admin (staff)
        self.user1 = dummy_user()
        self.user2 = dummy_user()
        self.admin = dummy_user(True)
        # Create a dummy category
        self.category = dummy_category()

    def check_permission(self, article, user, access):
        request = self.factory.get(article.get_absolute_url())
        request.user = user
        if access:
            self.assertEqual(view_article(request, article.id).status_code, 200)
        else:
            with self.assertRaises(Http404):
                view_article(request, article.id)

    def test_access_to_draft_article(self):
        article = dummy_article(self.user1, self.category, Article.DRAFT)
        self.check_permission(article, AnonymousUser(), False)
        self.check_permission(article, self.user1, True)
        self.check_permission(article, self.user2, False)
        self.check_permission(article, self.admin, True)

    def test_access_to_unapproved_article(self):
        article = dummy_article(self.user1, self.category, Article.UNAPPROVED)
        self.check_permission(article, AnonymousUser(), False)
        self.check_permission(article, self.user1, True)
        self.check_permission(article, self.user2, False)
        self.check_permission(article, self.admin, True)

    def test_access_to_published_article(self):
        article = dummy_article(self.user1, self.category, Article.PUBLISHED)
        self.check_permission(article, AnonymousUser(), True)
        self.check_permission(article, self.user1, True)
        self.check_permission(article, self.user2, True)
        self.check_permission(article, self.admin, True)
