import markdown


class LinkifyPattern(markdown.inlinepatterns.Pattern):
    """
    Pattern to replace bare links with <a> elements.
    """

    def __init__(self):
        super(LinkifyPattern, self).__init__(r'(https?:\/\/[^\s\b)]+)')

    def handleMatch(self, m):
        e = markdown.util.etree.Element('a')
        e.set('href', m.group(2))
        e.text = m.group(2)
        return e
