from django.utils.safestring import mark_safe
from markdown import Markdown

from twobuntu.cmarkdown.extension import TwobuntuExtension

cm = Markdown(safe_mode='escape', extensions=[
    'headerid',
    TwobuntuExtension({}),
])


def cmarkdown(value):
    """
    Render Markdown with our custom processors.

    :param value: raw markdown
    :returns: rendered HTML
    """
    return mark_safe(cm.convert(value))
