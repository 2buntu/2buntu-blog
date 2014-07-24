from hashlib import md5

from django import template

register = template.Library()


@register.filter()
def gravatar(email, size=64):
    """
    Return the Gravatar URL for the provided email.

    :param email: the email address to hash
    :param size: the size of the Gravatar to generate
    :returns: the URL of the image
    """
    return 'http://gravatar.com/avatar/%s?d=identicon&size=%s' % (
        md5(email).hexdigest(),
        size,
    )
