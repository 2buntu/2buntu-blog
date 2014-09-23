from django import forms


class DeviceArtForm(forms.Form):
    """
    Form for uploading an app screenshot.
    """

    image = forms.ImageField()
