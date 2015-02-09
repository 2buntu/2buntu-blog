from datetime import timedelta
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
        # Create a dummy user, category, and two articles for testing
        self.user = dummy_user()
        self.category = dummy_category()
        self.article1 = dummy_article(self.user, self.category, Article.PUBLISHED)
        self.article2 = dummy_article(self.user, self.category, Article.PUBLISHED)
        # Make the second article older so that the first one always sorts first
        self.article2.date -= timedelta(0, 1)
        self.article2.save()

    def check_response(self, num, view, viewargs={}, getargs={}):
        url = reverse(view, kwargs=viewargs)
        response = loads(smart_text(self.client.get(url, data=getargs).content))
        self.assertEqual(len(response), num)
        return response

    def check_error(self, view, **kwargs):
        self.assertTrue('error' in self.check_response(1, view, **kwargs))

    def test_methods(self):
        self.check_response(2, 'api:1.2:articles')
        self.check_response(1, 'api:1.2:article_by_id', viewargs={'id': self.article1.id})
        self.check_response(1, 'api:1.2:authors')
        self.check_response(1, 'api:1.2:author_by_id', viewargs={'id': self.user.id})
        self.check_response(2, 'api:1.2:articles_by_author', viewargs={'id': self.user.id})
        self.check_response(1, 'api:1.2:categories')
        self.check_response(2, 'api:1.2:articles_by_category', viewargs={'id': self.category.id})

    def test_page_size(self):
        self.check_response(1, 'api:1.2:articles', getargs={'size': 1})
        self.check_response(1, 'api:1.2:articles', getargs={'page': 2, 'size': 1})
        self.check_response(0, 'api:1.2:articles', getargs={'page': 3, 'size': 1})

    def test_min_max(self):
        past, future = 1, datetime_to_timestamp(now()) + 1
        self.check_response(2, 'api:1.2:articles', getargs={'min': past})
        self.check_response(2, 'api:1.2:articles', getargs={'max': future})
        self.check_response(0, 'api:1.2:articles', getargs={'min': future})
        self.check_response(0, 'api:1.2:articles', getargs={'max': past})

    def test_bad_input(self):
        for arg in ('min', 'max', 'page', 'size'):
            self.check_error('api:1.2:articles', getargs=dict(((arg, '-'),)))

    def test_jsonp(self):
        response = self.client.get(reverse('api:1.2:articles'), data={'callback': 'test'})
        self.assertEqual(smart_text(response.content)[0:5], 'test(')
