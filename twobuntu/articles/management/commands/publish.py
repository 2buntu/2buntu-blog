from __future__ import print_function

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
        articles = list(Article.objects.filter(scheduledarticle__date__lte=now()))
        for article in articles:
            article.status = Article.PUBLISHED
            article.save()
            print('"%s" published.' % article.title)
        print('%d article(s) published.' % len(articles))
