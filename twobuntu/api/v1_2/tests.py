from json import loads

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.encoding import smart_text
from django.utils.timezone import now

from twobuntu.articles.models import Article
from twobuntu.utils import datetime_to_timestamp, dummy_article, dummy_category, dummy_user


class TestAPI(TestCase):
    """
    Test that the API responds correctly to requests.
    """

    def setUp(self):
        # Create a dummy user, category, and article for testing
        self.user = dummy_user()
        self.category = dummy_category()
        self.article = dummy_article(self.user, self.category, Article.PUBLISHED)

    def get_response(self, view, viewargs={}, getargs={}, expected=1):
        url = reverse(view, kwargs=viewargs)
        response = loads(smart_text(self.client.get(url, data=getargs).content))
        self.assertEqual(len(response), expected)
        return response

    def test_methods(self):
        self.get_response('api:1.2:articles')
        self.get_response('api:1.2:article_by_id', viewargs={'id': self.article.id})
        self.get_response('api:1.2:authors')
        self.get_response('api:1.2:author_by_id', viewargs={'id': self.user.id})
        self.get_response('api:1.2:articles_by_author', viewargs={'id': self.user.id})
        self.get_response('api:1.2:categories')
        self.get_response('api:1.2:articles_by_category', viewargs={'id': self.category.id})

    def test_min_max(self):
        past, future = 1, datetime_to_timestamp(now()) + 1
        self.get_response('api:1.2:articles', getargs={'min': past})
        self.get_response('api:1.2:articles', getargs={'max': future})
        self.get_response('api:1.2:articles', expected=0, getargs={'min': future})
        self.get_response('api:1.2:articles', expected=0, getargs={'max': past})
