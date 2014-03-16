from hashlib import md5

from django import template

register = template.Library()

@register.filter()
def gravatar(email, size=64):
    """Return the Gravatar URL for the provided email."""
    return 'http://gravatar.com/avatar/%s?d=identicon&size=%s' % (
        md5(email).hexdigest(),
        size,
    )
