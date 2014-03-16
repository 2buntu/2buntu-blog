from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

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
                                              help_text="The current status of the article.")
    cc_license = models.BooleanField(default=True,
                                     help_text="Whether the article is released under the CC-BY-SA 4.0 license or not.")

    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Return a string representation of the article."""
        return '%s%s' % (
            self.title,
            ' [%s]' % self.get_status_display() if not self.status == self.PUBLISHED else '',
        )

    @models.permalink
    def get_absolute_url(self):
        """Return the absolute URL of the article."""
        return ('articles:view', (), {
            'id':   self.id,
            'slug': slugify(self.title),
        })

    def render(self):
        """Render the Markdown body."""
        return cmarkdown(self.body)

    class Meta:
        ordering = ('-date',)
