from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    """
    A grouping for articles of a similar topic.
    """

    name = models.CharField(
        max_length=40,
        help_text="The name of the category.",
    )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        """
        Return the absolute URL of the article.
        """
        return ('categories:view', (), {
            'id': self.id,
            'slug': slugify(self.name),
        })

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
