from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.timezone import now

class Profile(models.Model):
    """Information about an author."""

    user = models.OneToOneField(User,
                                primary_key=True)

    birthday = models.DateField(blank=True,
                                null=True,
                                help_text="The date that the user was born [used for displaying age].")
    location = models.CharField(max_length=40,
                                blank=True,
                                help_text="The geographic location of the user.")

    website = models.URLField(blank=True,
                              help_text="A website created or run by the user.")

    bio = models.TextField(blank=True,
                           help_text="A brief biography of the user.")

    def __unicode__(self):
        """Return a string representation of the profile."""
        return self.user.get_full_name() or self.user.get_username()

    def age(self):
        """Return the age of the user."""
        n, b = now().date(), self.birthday
        return n.year - b.year - (0 if n.month > b.month or n.month == b.month and n.day >= b.day else 1)

    @models.permalink
    def get_absolute_url(self):
        """Return the absolute URL of the profile."""
        return ('accounts:profile', (), {
            'id':   self.user.id,
            'slug': slugify(self),
        })

@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a profile whenever a user is created."""
    if created:
        Profile.objects.create(user=instance)

class ConfirmationKey(models.Model):
    """Unique token for confirming a user account or resetting a password."""

    user = models.OneToOneField(User,
                                primary_key=True)
    key = models.CharField(max_length=32,
                           default=lambda:uuid4().hex)

    def __unicode__(self):
        """Return a string representation of the key."""
        return self.user
