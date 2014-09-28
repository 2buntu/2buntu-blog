from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Publisher(models.Model):
    """
    An application publisher.
    """

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Department(models.Model):
    """
    An application category.
    """

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Keyword(models.Model):
    """
    A descriptive keyword.
    """

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Application(models.Model):
    """
    An Ubuntu Touch application.
    """

    # Although an integer would make a better primary key, the identity of the
    # app is literally tied to this identifier, which is guaranteed to be unique
    name = models.CharField(
        max_length=100,
        primary_key=True,
    )

    icon_url = models.ImageField(upload_to='apps/icons')

    title = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    description = models.TextField()
    license = models.CharField(max_length=40)

    website = models.URLField()
    download_url = models.URLField()
    download_size = models.PositiveIntegerField()

    publisher = models.ForeignKey(Publisher)
    department = models.ForeignKey(Department)
    keywords = models.ManyToManyField(Keyword)

    rating = models.PositiveSmallIntegerField()

    last_updated = models.DateTimeField()
    date_published = models.DateTimeField()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Screenshot(models.Model):
    """
    A screenshot for an application.
    """

    application = models.ForeignKey(Application)
    image = models.ImageField(upload_to='apps/screenshots')

    def __str__(self):
        return self.application.title
