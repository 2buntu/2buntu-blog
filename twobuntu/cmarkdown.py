import markdown
import re

from django.db.models import get_model
from django.utils.safestring import mark_safe


class LinkifyPattern(markdown.inlinepatterns.Pattern):
    """
    Pattern to replace bare links with <a> elements.
    """

    def __init__(self):
        super(LinkifyPattern, self).__init__(r'(https?:\/\/[^\s\b]+)')

    def handleMatch(self, m):
        e = markdown.util.etree.Element('a')
        e.set('href', m.group(2))
        e.text = m.group(2)
        return e


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
        Model = get_model(*self.MODEL)
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
            e.text = unicode(article)
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


class AlertProcessor(markdown.blockprocessors.BlockProcessor):
    """
    Block processor to display alert boxes.
    """

    TAGS = {
        'info': 'info-circle',
        'warning': 'warning',
        'danger': 'bomb',
    }
    PATTERN = re.compile(r'\[(%s)\]' % '|'.join(TAGS.keys()))

    def test(self, parent, block):
        return self.PATTERN.search(block)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        open_match = self.PATTERN.search(block)
        tag = open_match.group(1)
        # Have the parser parse everything before the opening tag
        self.parser.parseBlocks(parent, [block[:open_match.start()]])
        # Build a list of blocks inside the tag
        content = [block[open_match.end():]]
        # Search for the appropriate closing tag
        close_pattern = re.compile(r'\[/%s\]' % tag)
        while True:
            close_match = close_pattern.search(content[-1])
            if close_match:
                # Remove the closing tag and trailing text from the last block
                last_block = content.pop(-1)
                content.append(last_block[:close_match.start()])
                # Create the alert element and parse the blocks inside the alert body
                self.parser.parseBlocks(self._create_alert(parent, tag), content)
                # Insert the remaining text back into the block list
                blocks.insert(0, last_block[close_match.end():])
                break
            # If closing tag is missing, make it implicit
            if not len(blocks):
                content.append('[/%s]' % tag)
            else:
                content.append(blocks.pop(0))

    def _create_alert(self, parent, tag):
        alert = markdown.util.etree.SubElement(parent, 'div')
        alert.set('class', 'alert alert-%s' % tag)
        media = markdown.util.etree.SubElement(alert, 'div')
        media.set('class', 'media')
        icon = markdown.util.etree.SubElement(media, 'span')
        icon.set('class', 'fa fa-3x fa-%s media-object pull-left' % self.TAGS[tag])
        body = markdown.util.etree.SubElement(media, 'div')
        body.set('class', 'media-body')
        return body


class TwoBuntuExtension(markdown.Extension):
    """
    Custom Markdown extension for 2buntu.
    """

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add(
            'strikethrough',
            markdown.inlinepatterns.SimpleTagPattern(r'---([^-]+)---', 's'),
            '_end'
        )
        md.inlinePatterns.add('linkify', LinkifyPattern(), '_end')
        md.inlinePatterns.add('article', ArticlePattern(), '_end')
        md.inlinePatterns.add('image', ImagePattern(), '_end')
        md.parser.blockprocessors.add('alert', AlertProcessor(md.parser), '_begin')


cm = markdown.Markdown(safe_mode='escape', extensions=[
    'headerid',
    TwoBuntuExtension({}),
])


def cmarkdown(value):
    """
    Render Markdown with our custom processors.

    :param value: raw markdown
    :returns: rendered HTML
    """
    return mark_safe(cm.convert(value))
