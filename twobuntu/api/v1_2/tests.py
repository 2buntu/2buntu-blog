from json import loads

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.encoding import smart_text

from twobuntu.articles.models import Article
from twobuntu.utils import dummy_article, dummy_category, dummy_user


class TestAPI(TestCase):
    """
    Test that the API responds correctly to requests.
    """

    def setUp(self):
        # Create a dummy user, category, and article for testing
        self.user = dummy_user()
        self.category = dummy_category()
        self.article = dummy_article(self.user, self.category, Article.PUBLISHED)

    def get_response(self, view, expected=1, **kwargs):
        url = reverse(view, kwargs=kwargs)
        response = loads(smart_text(self.client.get(url).content))
        self.assertEqual(len(response), expected)
        return response

    def test_methods(self):
        # Ensure all of the methods return a single response when appropriate
        self.get_response('api:1.2:articles')
        self.get_response('api:1.2:article_by_id', id=self.article.id)
        self.get_response('api:1.2:authors')
        self.get_response('api:1.2:author_by_id', id=self.user.id)
        self.get_response('api:1.2:articles_by_author', id=self.user.id)
        self.get_response('api:1.2:categories')
        self.get_response('api:1.2:articles_by_category', id=self.category.id)
