from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from twobuntu.categories.models import Category
from twobuntu.cmarkdown import cmarkdown
from twobuntu.images.models import Image


@python_2_unicode_compatible
class Article(models.Model):
    """
    A post written in Markdown by an author.
    """

    # Article status constants
    DRAFT = 0
    UNAPPROVED = 1
    PUBLISHED = 2

    STATUS = (
        (DRAFT, 'Draft'),
        (UNAPPROVED, 'Unapproved'),
        (PUBLISHED, 'Published'),
    )

    author = models.ForeignKey(
        User,
        help_text="The user writing the article.",
    )
    category = models.ForeignKey(
        Category,
        help_text="The category of the article.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The title of the article.",
    )
    body = models.TextField(help_text="The body of the article [in Markdown].")
    image = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        help_text="An image highlighting the contents of the article.",
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=DRAFT,
        help_text="The current status of the article.",
    )
    cc_license = models.BooleanField(
        default=True,
        help_text="Whether the article is released under the CC-BY-SA 4.0 license or not.",
    )
    date = models.DateTimeField()

    def __str__(self):
        return '%s%s' % (
            self.title,
            ' [%s]' % self.get_status_display() if not self.status == self.PUBLISHED else '',
        )

    @models.permalink
    def get_absolute_url(self):
        kwargs, slug = {'id': self.id}, slugify(self.title)
        if slug:
            kwargs['slug'] = slug
        return ('articles:view', (), kwargs)

    def can_edit(self, request):
        """
        Determine if the article may be edited by the current user.
        """
        # The user must either be staff or have written the article and not published it yet
        return request.user.is_staff or request.user == self.author and self.status == self.DRAFT

    def can_view(self, request):
        """
        Determine if the article may be viewed by the current user.
        """
        # The user must either be staff or have written the article or it must be published
        return request.user.is_staff or request.user == self.author or self.status == self.PUBLISHED

    @property
    def markdown_key(self):
        """
        Return the key used for caching markdown.
        """
        return 'article-%d-markdown' % self.id

    def related(self):
        """
        Returns a QuerySet of related articles.
        """
        return Article.objects.filter(~models.Q(id=self.id), status=self.PUBLISHED, category=self.category)

    def render(self):
        """
        Render the Markdown body.
        """
        md = cache.get(self.markdown_key)
        if not md:
            md = cmarkdown(self.body)
            cache.set(self.markdown_key, md)
        return md

    @classmethod
    def apply_filter(cls, request, *args):
        """
        Return a QuerySet with the correct filter applied based on the request.
        """
        args = list(args)
        if not request.user.is_staff:
            args.append(models.Q(author=request.user.id) | models.Q(status=cls.PUBLISHED))
        return cls.objects.filter(*args)

    class Meta:
        ordering = ('status', '-date')


@receiver(models.signals.post_init, sender=Article)
def set_status(instance, **kwargs):
    """
    Store the status of the article before it is modified.
    """
    instance.old_status = instance.status


@receiver(models.signals.pre_save, sender=Article)
def update_date(instance, **kwargs):
    """
    Update the date if required.
    """
    if not instance.status == instance.old_status == Article.PUBLISHED:
        instance.date = now()


@python_2_unicode_compatible
class ScheduledArticle(models.Model):
    """
    An article to be published at a later date.
    """

    article = models.OneToOneField(
        Article,
        primary_key=True,
    )
    date = models.DateTimeField(help_text="Date/time to publish article (YYYY-MM-DD HH:MM:SS).")

    def __str__(self):
        return unicode(self.article)


@receiver(models.signals.post_save, sender=Article)
def clear_cache_and_remove_scheduled(instance, created, **kwargs):
    """
    Clear the cache and remove any scheduled articles instance.
    """
    if not created:
        cache.delete(instance.markdown_key)
    if instance.status == Article.PUBLISHED:
        ScheduledArticle.objects.filter(article=instance).delete()
