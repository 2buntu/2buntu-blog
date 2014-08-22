from uuid import uuid4

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ShortURL(models.Model):
    """
    A short URL for redirection.
    """

    key = models.CharField(
        max_length=6,
        primary_key=True,
        default=lambda: uuid4().hex[:6],
    )
    url = models.URLField(help_text="URL to redirect the client to.")

    def __str__(self):
        return self.url
