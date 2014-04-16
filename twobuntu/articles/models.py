from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.timezone import now

from twobuntu.categories.models import Category
from twobuntu.cmarkdown import cmarkdown

class Article(models.Model):
    """A post written in Markdown by an author."""

    # Article status constants
    DRAFT      = 0
    UNAPPROVED = 1
    PUBLISHED  = 2

    STATUS = (
        (DRAFT,      'Draft',),
        (UNAPPROVED, 'Unapproved',),
        (PUBLISHED,  'Published',),
    )

    author = models.ForeignKey(User,
                               help_text="The user writing the article.")
    category = models.ForeignKey(Category,
                                 help_text="The category of the article.")

    title = models.CharField(max_length=200,
                             help_text="The title of the article.")
    body = models.TextField(help_text="The body of the article [in Markdown].")

    status = models.PositiveSmallIntegerField(choices=STATUS,
                                              default=DRAFT,
                                              help_text="The current status of the article.")
    cc_license = models.BooleanField(default=True,
                                     help_text="Whether the article is released under the CC-BY-SA 4.0 license or not.")

    date = models.DateTimeField()

    def __unicode__(self):
        """Return a string representation of the article."""
        return '%s%s' % (
            self.title,
            ' [%s]' % self.get_status_display() if not self.status == self.PUBLISHED else '',
        )

    def can_edit(self, request):
        """Determine if the article may be edited by the current user."""
        # The user must either be staff or have written the article and not published it yet
        return request.user.is_staff or request.user == self.author and self.status == self.DRAFT

    def can_view(self, request):
        """Determine if the article may be viewed by the current user."""
        # The user must either be staff or have written the article or it must be published
        return request.user.is_staff or request.user == self.author or self.status == self.PUBLISHED

    @classmethod
    def apply_filter(cls, request, *args):
        """Return a QuerySet with the correct filter applied based on the request."""
        args = list(args)
        if not request.user.is_staff:
            args.append(models.Q(author=request.user.id) | models.Q(status=cls.PUBLISHED))
        return cls.objects.filter(*args)

    @models.permalink
    def get_absolute_url(self):
        """Return the absolute URL of the article."""
        return ('articles:view', (), {
            'id':   self.id,
            'slug': slugify(self.title),
        })

    def render(self):
        """Render the Markdown body."""
        md = cache.get(self.id)
        if not md:
            md = cmarkdown(self.body)
            cache.set(self.id, md)
        return md

    class Meta:
        ordering = ('status', '-date',)

@receiver(models.signals.post_init, sender=Article)
def set_status(instance, **kwargs):
    """Store the status of the article before it is modified."""
    instance.old_status = instance.status

@receiver(models.signals.pre_save, sender=Article)
def clear_cache_and_set_date(instance, **kwargs):
    """Clear the rendered cache and update the date if required."""
    cache.delete(instance.id)
    if not instance.status == instance.old_status == Article.PUBLISHED:
        instance.date = now()
