from django.db import models

class Image(models.Model):
    """A web-accessible image file."""

    caption = models.CharField(max_length=100,
                               help_text="A brief description of the image.")
    image = models.ImageField(upload_to='images',
                              help_text="The image file.")
    
    def __unicode__(self):
        """Return a string representation of the image."""
        return self.caption
    
    @models.permalink
    def get_absolute_url(self):
        """Return the absolute URL of the image."""
        return ('images:view', (), {
            'id': self.id,
        })
