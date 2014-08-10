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
        super(ImagePattern, self).__init__(r'\[image:\s*(\d+)(:primary)?\]')

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

    TAGS = {
        'info': 'info-circle',
        'warning': 'warning',
        'danger': 'bomb',
    }
    PATTERN = re.compile(r'\[(%s)\]' % '|'.join(TAGS.keys()))

    def test(self, parent, block):
        """
        Identify the type of block.
        """
        return self.PATTERN.search(block)

    def run(self, parent, blocks):
        """
        Perform any necessary substitutions.
        """
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
                # Parse the text after the closing tag
                self.parser.parseBlocks(parent, [last_block[close_match.end():]])
                break
            # If closing tag is missing, make it implicit
            if not len(blocks):
                content.append('[/%s]' % tag)
            else:
                content.append(blocks.pop(0))

    def _create_alert(self, parent, tag):
        """
        Create the container for the content.
        """
        alert = markdown.util.etree.SubElement(parent, 'div')
        alert.set('class', 'alert alert-%s' % tag)
        media = markdown.util.etree.SubElement(alert, 'div')
        media.set('class', 'media')
        icon = markdown.util.etree.SubElement(media, 'span')
        icon.set('class', 'fa fa-4x fa-%s media-object pull-left' % self.TAGS[tag])
        body = markdown.util.etree.SubElement(media, 'div')
        body.set('class', 'media-body')
        return body


class TwoBuntuExtension(markdown.Extension):
    """
    Custom Markdown extension for 2buntu.
    """

    def extendMarkdown(self, md, md_globals):
        """
        Add our custom processors to the Markdown parser.
        """
        strikethrough_pattern = markdown.inlinepatterns.SimpleTagPattern(r'---([^-]+)---', 's')
        md.inlinePatterns.add('strikethrough', strikethrough_pattern, '_end')
        md.inlinePatterns.add('linkify', LinkifyPattern(), '_end')
        md.inlinePatterns.add('image', ImagePattern(), '_end')
        md.parser.blockprocessors.add('alert', AlertProcessor(md.parser), '_begin')


cm = markdown.Markdown(safe_mode='escape', extensions=[
    'headerid',
    TwoBuntuExtension({}),
])


def cmarkdown(value):
    """
    Render Markdown with our custom processors.
    """
    return mark_safe(cm.convert(value))
