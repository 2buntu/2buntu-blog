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
        # Create a dummy article for testing
        self.article = dummy_article(self.user1, dummy_category())

    def request(self, user):
        request = self.factory.get(self.article.get_absolute_url())
        request.user = user
        return view_article(request, self.article.id)

    def check_permission(self, user, access):
        if access:
            self.assertEqual(self.request(user).status_code, 200)
        else:
            with self.assertRaises(Http404):
                self.request(user)

    def test_access_to_draft_article(self):
        self.article.status = Article.DRAFT
        self.article.save()
        self.check_permission(AnonymousUser(), False)
        self.check_permission(self.user1, True)
        self.check_permission(self.user2, False)
        self.check_permission(self.admin, True)

    def test_access_to_unapproved_article(self):
        self.article.status = Article.UNAPPROVED
        self.article.save()
        self.check_permission(AnonymousUser(), False)
        self.check_permission(self.user1, True)
        self.check_permission(self.user2, False)
        self.check_permission(self.admin, True)

    def test_access_to_published_article(self):
        self.article.status = Article.PUBLISHED
        self.article.save()
        self.check_permission(AnonymousUser(), True)
        self.check_permission(self.user1, True)
        self.check_permission(self.user2, True)
        self.check_permission(self.admin, True)
