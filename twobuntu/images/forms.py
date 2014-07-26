from django import forms

from twobuntu.images.models import Image


class ImageUploadForm(forms.ModelForm):
    """
    Form for uploading images.
    """

    class Meta:
        model = Image
        fields = ('caption', 'image')
