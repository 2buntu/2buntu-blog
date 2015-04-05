from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils.encoding import smart_bytes, smart_text
from django.utils.timezone import now

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category
from twobuntu.cmarkdown import cmarkdown as cm
from twobuntu.images.models import Image


class TestCMarkdown(TestCase):
    """
    Test that custom Markdown is correctly rendered.
    """

    def setUp(self):
        # Create a dummy user, category, and article
        user = User.objects.create_user('user', 'user@example.com', 'user')
        category = Category(name='Test')
        category.save()
        self.article = Article(author=user, category=category, title='Test', body='Test', status=Article.PUBLISHED, date=now())
        self.article.save()
        # Create a dummy image
        o = BytesIO(smart_bytes('x\x9cb`\x01\x00\x00\x00\xff\xff\x03\x00\x00\x06\x00\x05'))
        self.image = Image(caption='Test', image=File(o, name='test.png'))
        self.image.save()

    def test_basic_markup(self):
        self.assertEqual(cm('**test**'), '<p><strong>test</strong></p>')
        self.assertEqual(cm('# Test'), '<h1 id="test">Test</h1>')
        self.assertEqual(cm('[test](http://example.org)'), '<p><a href="http://example.org">test</a></p>')
        self.assertEqual(cm('`test`'), '<p><code>test</code></p>')

    def test_linkify(self):
        self.assertEqual(cm('http://example.org'), '<p><a href="http://example.org">http://example.org</a></p>')

    def test_references(self):
        self.assertEqual(cm('[article:%d]' % self.article.id), '<p><a href="/articles/%d/test/">Test</a></p>' % self.article.id)
        self.assertEqual(cm('[image:%d]' % self.image.id), '<p><img alt="Test" src="%s" title="Test" /></p>' % self.image.image.url)

    def test_alerts(self):
        self.assertEqual(
            cm('[info]test[/info]'),
            '<div class="alert alert-info">\n<div class="media">' +
            '<span class="fa fa-3x fa-info-circle media-object pull-left">' +
            '</span><div class="media-body">\n<p>test</p>\n</div>\n</div>\n</div>'
        )

    def test_strikethrough(self):
        self.assertEqual(cm('---test---'), '<p><s>test</s></p>')

    def test_escaping(self):
        self.assertEqual(cm('<>'), '<p>&lt;&gt;</p>')

    def test_unicode(self):
        self.assertEqual(cm(smart_text('\xce\xa9')), smart_text('<p>\xce\xa9</p>'))
