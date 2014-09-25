from django import forms


class DeviceArtForm(forms.Form):
    """
    Form for uploading an app screenshot.
    """

    image = forms.ImageField()
    add_panel = forms.BooleanField(required=False, label='Add the Unity panel to the picture')
