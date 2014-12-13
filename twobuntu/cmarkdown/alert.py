import markdown
import re


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
