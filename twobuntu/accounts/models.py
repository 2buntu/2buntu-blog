from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from twobuntu.utils import uuid


@python_2_unicode_compatible
class Profile(models.Model):
    """
    Information about an author.
    """

    user = models.OneToOneField(
        User,
        primary_key=True,
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        help_text="Birthday in YYYY-MM-DD format [used for displaying age].",
    )
    location = models.CharField(
        max_length=40,
        blank=True,
        help_text="Geographic location.",
    )
    website = models.URLField(
        blank=True,
        help_text="A personal blog or website.",
    )
    bio = models.TextField(
        blank=True,
        help_text="A brief biography.",
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()

    @models.permalink
    def get_absolute_url(self):
        kwargs, slug = {'id': self.user.id}, slugify(self)
        if slug:
            kwargs['slug'] = slug
        return ('accounts:profile', (), kwargs)

    def age(self):
        """
        Calculate the age of the user.
        """
        if not self.birthday:
            return None
        n, b = now().date(), self.birthday
        return n.year - b.year - (0 if n.month > b.month or n.month == b.month and n.day >= b.day else 1)

    class Meta:
        ordering = ('-user__last_login',)


@receiver(models.signals.post_save, sender=User)
def create_profile(instance, created, **kwargs):
    """
    Create a profile whenever a user is created.
    """
    if created:
        Profile.objects.create(user=instance)


@python_2_unicode_compatible
class ConfirmationKey(models.Model):
    """
    Unique token for confirming a user account or resetting a password.
    """

    user = models.OneToOneField(
        User,
        primary_key=True,
    )
    key = models.CharField(
        max_length=32,
        default=uuid,
    )

    def __str__(self):
        return self.user
