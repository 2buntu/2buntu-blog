from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Completely clear the cache.

    Do NOT use this command when it is not necessary since it will immediately
    result in a spike of markdown rendering due to incoming requests.
    """

    help = "Completely clear the cache."

    def handle(self, *args, **kwargs):
        """
        Process the command.
        """
        cache.clear()
        self.stdout.write("Cache has been completely cleared.")
