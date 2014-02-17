from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    """A short news report."""

    reporter = models.ForeignKey(User,
                                 help_text="The user reporting the news item.")

    title = models.CharField(max_length=100,
                             help_text="The title of the news item.")
    body = models.TextField(help_text="The body of the news item [in Markdown].")

    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        """Return a string representation of the news item."""
        return self.title

    class Meta:
        ordering = ('-date',)
