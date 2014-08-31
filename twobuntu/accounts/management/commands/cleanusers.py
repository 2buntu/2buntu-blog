from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.timezone import now


class Command(BaseCommand):
    """
    Remove inactive users.

    Deletes all users that have never published an article and have not logged
    in during the previous month.
    """

    help = "Remove inactive users."
    output_transaction = True

    def handle(self, *args, **kwargs):
        """
        Process the command.
        """
        month = now() - relativedelta(months=1)  # determine one month ago
        users = list(User.objects.annotate(num_articles=Count('article')).filter(num_articles=0, last_login__lte=month))
        for user in users:
            user.delete()
            self.stdout.write('User "%s" deleted.' % user)
        self.stdout.write("%d user(s) deleted." % len(users))
