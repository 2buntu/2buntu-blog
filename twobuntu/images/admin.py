from django.contrib import admin

from twobuntu.images.models import Image


class ImageAdmin(admin.ModelAdmin):
    """
    Describe the administration inferface for images.
    """

    search_fields = ('caption', 'image')


admin.site.register(Image, ImageAdmin)
