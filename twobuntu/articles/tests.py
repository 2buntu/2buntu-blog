from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils.timezone import now

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category


class TestArticlePermission(TestCase):
    """
    Test that the correct users have access to the correct articles.
    """

    def setUp(self):
        # Create three users - two normal users and an admin (staff)
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

    def create_request(self, article, username=None):
        client = Client()
        if username:
            client.login(username=username, password=username)
        return client.get(article.get_absolute_url())

    def test_access_to_draft_article(self):
        response = self.create_request(self.draft_article)
        self.assertEqual(response.status_code, 404)
