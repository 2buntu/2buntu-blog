from uuid import uuid4

from django.db import models

class ShortURL(models.Model):
    """A short URL for redirection."""

    key = models.CharField(max_length=6,
                           primary_key=True,
                           default=lambda:uuid4().hex[:6])

    url = models.URLField(help_text="URL to redirect the client to.")

    def __unicode__(self):
        """Return a string representation of the URL."""
        return self.url
