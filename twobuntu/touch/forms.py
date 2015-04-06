from django import forms

from twobuntu.touch.generator import TEMPLATES


class DeviceArtForm(forms.Form):
    """
    Form for uploading an app image.
    """

    template = forms.TypedChoiceField(
        initial='bq-aquaris',
        choices=[(k, TEMPLATES[k]['title']) for k in sorted(TEMPLATES.keys())],
    )
    add_panel = forms.BooleanField(
        label="Add Unity panel",
        required=False,
        help_text='Remember to take into account the height of the panel when uploading the image.',
    )
    glossy_screen = forms.BooleanField(
        required=False,
        initial=True,
    )
    image = forms.ImageField()
