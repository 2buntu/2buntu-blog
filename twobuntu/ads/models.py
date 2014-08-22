from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Ad(models.Model):
    """
    An advertisement for a product.
    """

    product = models.CharField(
        max_length=100,
        help_text="The name of the product being advertised.",
    )
    image = models.ImageField(
        upload_to='ads',
        help_text="An image depicting the advertised product.",
    )
    url = models.URLField(help_text="The URL that will be displayed when the image is selected.")
    display_start = models.DateTimeField(help_text="When the ad should start being displayed.")
    display_end = models.DateTimeField(help_text="When the ad should stop being displayed.")

    def __str__(self):
        return self.product
