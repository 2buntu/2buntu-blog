from django import forms

from twobuntu.touch.generator import TEMPLATES


class DeviceArtForm(forms.Form):
    """
    Form for uploading an app image.
    """

    template = forms.TypedChoiceField(
        choices=[(i, t['title']) for i, t in enumerate(TEMPLATES)],
        coerce=int,
    )
    image = forms.ImageField()
