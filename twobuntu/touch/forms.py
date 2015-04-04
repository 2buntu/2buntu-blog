from django import forms

from twobuntu.touch.generator import TEMPLATES


class DeviceArtForm(forms.Form):
    """
    Form for uploading an app image.
    """

    template = forms.TypedChoiceField(
        choices=[(t['name'], t['title']) for t in TEMPLATES],
        coerce=int,
    )
    add_panel = forms.BooleanField(
        label="Add Unity panel",
        required=False,
    )
    glossy_screen = forms.BooleanField(
        required=False,
        initial=True,
    )
    image = forms.ImageField()
