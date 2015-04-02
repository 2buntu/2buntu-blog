import markdown

from django.apps import apps
from django.utils.encoding import smart_text


class ReferencePattern(markdown.inlinepatterns.Pattern):
    """
    Pattern to recognize references to internal model instances.

    Subclasses are expected to have two class attributes - MODEL_NAME, which is
    used in the pattern, and MODEL, a string in dotted notation referencing the
    model class. Subclasses must also provide a create_element method.
    """

    def __init__(self):
        super(ReferencePattern, self).__init__(r'\[%s:(\d+)\]' % self.MODEL_NAME)

    def handleMatch(self, m):
        Model = apps.get_model(*self.MODEL)
        instance = None
        try:
            instance = Model.objects.get(pk=m.group(2))
        except Model.DoesNotExist:
            pass
        e = instance and self.create_element(instance)
        if e is None:
            e = markdown.util.etree.Element('p')
            e.set('class', 'text-muted')
            e.text = '[Invalid %s reference.]' % self.MODEL_NAME
        return e


class ArticlePattern(ReferencePattern):
    """
    Pattern to replace references to other articles with <a> elements.
    """

    MODEL_NAME = 'article'
    MODEL = ('articles', 'Article')

    def create_element(self, article):
        # Note: only published articles are rendered
        if article.status == article.PUBLISHED:
            e = markdown.util.etree.Element('a')
            e.set('href', article.get_absolute_url())
            e.text = smart_text(article)
            return e


class ImagePattern(ReferencePattern):
    """
    Pattern to replace references to images with <img> elements.
    """

    MODEL_NAME = 'image'
    MODEL = ('images', 'Image')

    def create_element(self, image):
        e = markdown.util.etree.Element('img')
        e.set('src', image.image.url)
        e.set('alt', image.caption)
        e.set('title', image.caption)
        return e
