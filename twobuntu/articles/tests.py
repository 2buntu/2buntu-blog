from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.utils.timezone import now

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category


class TestArticlePermission(TestCase):
    """
    Test that the correct users have access to the correct articles.
    """

    def setUp(self):
        # Create a client that will be used for making requests
        self.client = Client()
        # Create three users - an anonymous user, a normal user, and an admin (staff)
        self.anonymous_user = AnonymousUser()
        self.ordinary_user1 = User.objects.create_user('ordinary1', 'ordinary1@example.com', 'ordinary1')
        self.ordinary_user2 = User.objects.create_user('ordinary2', 'ordinary1@example.com', 'ordinary2')
        self.administrator = User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.administrator.is_staff = True
        self.administrator.save()
        # Create a dummy category for the articles
        self.category = Category(name='Test')
        self.category.save()
        # Create articles in various stages of completion
        self.draft_article = self.create_article()
        self.unapproved_article = self.create_article(status=Article.UNAPPROVED)
        self.published_article = self.create_article(status=Article.PUBLISHED)

    def create_article(self, **kwargs):
        article = Article(author=self.ordinary_user1, category=self.category, title='Test', body='Test', date=now(), **kwargs)
        article.save()
        return article

    def test_access_to_draft_article(self):
        response = self.client.get(self.draft_article.get_absolute_url())
        self.assertEqual(response.status_code, 404)
