import twitter
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Item(models.Model):
    """
    A short news report.
    """

    reporter = models.ForeignKey(
        User,
        help_text="The user reporting the news item.",
    )
    title = models.CharField(
        max_length=100,
        help_text="The title of the news item.",
    )
    body = models.TextField(
        help_text="The body of the news item [in Markdown].",
    )
    url = models.URLField(help_text="URL with more details about the news item.")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-date',)


# Create a global Twitter API object used for tweeting
_api = twitter.Api(**settings.TWITTER)


@receiver(models.signals.post_save, sender=Item)
def post_tweet(instance, created, **kwargs):
    """
    Post a tweet when a news item is created.
    """
    if created:
        _api.PostUpdate('%s %s' % (
            instance.title,
            instance.url,
        ))
