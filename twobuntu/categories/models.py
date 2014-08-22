from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    """
    A grouping for articles of a similar topic.
    """

    name = models.CharField(
        max_length=40,
        help_text="The name of the category.",
    )
    image = models.ImageField(
        upload_to='categories',
        blank=True,
        null=True,
        help_text="A representative image.",
    )

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('categories:view', (), {
            'id': self.id,
            'slug': slugify(self.name),
        })

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
