import markdown

from twobuntu.cmarkdown.alert import AlertProcessor
from twobuntu.cmarkdown.linkify import LinkifyPattern
from twobuntu.cmarkdown.reference import ArticlePattern, ImagePattern


class TwobuntuExtension(markdown.Extension):
    """
    Custom Markdown extension for 2buntu.
    """

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add(
            'strikethrough',
            markdown.inlinepatterns.SimpleTagPattern(r'(---)([^-]+)(---)', 's'),
            '_end'
        )
        md.inlinePatterns.add('linkify', LinkifyPattern(), '_end')
        md.inlinePatterns.add('article', ArticlePattern(), '_end')
        md.inlinePatterns.add('image', ImagePattern(), '_end')
        md.parser.blockprocessors.add('alert', AlertProcessor(md.parser), '_begin')
