from django.core.management.base import BaseCommand
from django.utils.timezone import now

from twobuntu.articles.models import Article


class Command(BaseCommand):
    """
    Publish all scheduled articles dated in the past.
    """

    help = "Publish all scheduled articles."
    output_transaction = True

    def handle(self, *args, **kwargs):
        """
        Process the command.
        """
        articles = list(Article.objects.filter(scheduledarticle__date__lte=now()))
        for article in articles:
            article.status = Article.PUBLISHED
            article.save()
            self.stdout.write('"%s" published.' % article)
        self.stdout.write("%d article(s) published." % len(articles))
