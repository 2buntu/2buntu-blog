import markdown
import re

from django.utils.safestring import mark_safe

from twobuntu.images.models import Image


class LinkifyPattern(markdown.inlinepatterns.Pattern):
    """
    Pattern to replace bare links with <a> elements.
    """

    def __init__(self):
        """
        Initialize the pattern.
        """
        super(LinkifyPattern, self).__init__(r'(https?:\/\/[^\s\b]+)')

    def handleMatch(self, m):
        """
        Process a match of the regular expression.
        """
        e = markdown.util.etree.Element('a')
        e.set('href', m.group(2))
        e.text = m.group(2)
        return e


class ImagePattern(markdown.inlinepatterns.Pattern):
    """
    Pattern to replace references to images with <img> elements.
    """

    def __init__(self):
        """
        Initialize the pattern.
        """
        super(ImagePattern, self).__init__(r'\[image:\s*(\d+)\]')

    def handleMatch(self, m):
        """
        Process a match of the regular expression.
        """
        try:
            img = Image.objects.get(pk=m.group(2))
        except IndexError, Image.DoesNotExist:
            pass
        else:
            e = markdown.util.etree.Element('img')
            e.set('src', img.image.url)
            e.set('title', img.caption)
            return e


class AlertProcessor(markdown.blockprocessors.BlockProcessor):
    """
    Block processor to display alert boxes.
    """

    TAGS = ['info', 'warning', 'danger']
    PATTERN = re.compile(r'^\[(%s)\](.*)\[/\1\]$' % '|'.join(TAGS), re.DOTALL)

    def test(self, parent, block):
        """
        Identify the type of block.
        """
        return self.PATTERN.match(block)

    def run(self, parent, blocks):
        """
        Perform any necessary substitutions.
        """
        t, r = self.PATTERN.match(blocks.pop(0)).groups()
        e = markdown.util.etree.SubElement(parent, 'div')
        e.set('class', 'alert alert-%s' % t)
        e.text = r
        i = markdown.util.etree.SubElement(e, 'span')
        i.set('class', 'sprite sprite-icon sprite-icon-%s' % t)


class TwoBuntuExtension(markdown.Extension):
    """
    Custom Markdown extension for 2buntu.
    """

    def extendMarkdown(self, md, md_globals):
        """
        Add our custom processors to the Markdown parser.
        """
        md.inlinePatterns.add('linkify', LinkifyPattern(), '_end')
        md.inlinePatterns.add('image', ImagePattern(), '_end')
        md.parser.blockprocessors.add('alert', AlertProcessor(md.parser), '>indent')


cm = markdown.Markdown(safe_mode='escape', extensions=[
    'headerid(level=3)',
    TwoBuntuExtension({}),
])


def cmarkdown(value):
    """
    Render Markdown with our custom processors.
    """
    return mark_safe(cm.convert(value))
