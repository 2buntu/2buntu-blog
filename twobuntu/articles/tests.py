from django.contrib.auth.models import AnonymousUser, User
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import now

from twobuntu.articles.models import Article
from twobuntu.articles.views import view as view_article
from twobuntu.categories.models import Category


class TestArticlePermission(TestCase):
    """
    Test that the correct users have access to the correct articles.
    """

    def setUp(self):
        # Create the request factory
        self.factory = RequestFactory()
        # Create three users - two normal users and an admin (staff)
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'user1')
        self.user2 = User.objects.create_user('user2', 'user1@example.com', 'user2')
        self.admin = User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.admin.is_staff = True
        self.admin.save()
        # Create a dummy category for the articles
        self.category = Category(name='Test')
        self.category.save()
        # Create a dummy article for testing
        self.article = Article(author=self.user1, category=self.category, title='Test', body='Test', date=now())

    def request(self, article, user):
        request = self.factory.get(article.get_absolute_url())
        request.user = user
        return view_article(request, article.id)

    def check_permission(self, user, access):
        if access:
            self.assertEqual(self.request(self.article, user).status_code, 200)
        else:
            with self.assertRaises(Http404):
                self.request(self.article, user)

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
