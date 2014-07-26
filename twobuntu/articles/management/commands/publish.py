from django.core.management.base import BaseCommand
from django.utils.timezone import now

from twobuntu.articles.models import Article


class Command(BaseCommand):
    """
    Publish all scheduled articles dated in the past.
    """

    help = "Publish all scheduled articles."

    def handle(self, *args, **kwargs):
        """
        Process the command.
        """
        for article in Article.objects.filter(scheduledarticle__date__lte=now()):
            article.status = Article.PUBLISHED
            article.save()
            print '"%s" published.' % article.title
