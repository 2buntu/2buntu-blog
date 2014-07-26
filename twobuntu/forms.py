from django import forms
from captcha.fields import ReCaptchaField


class FeedbackForm(forms.Form):
    """
    Form for user feedback.
    """

    name = forms.CharField()
    email = forms.CharField(
        required=False,
        help_text="Not required unless you would like a reply.",
    )
    comments = forms.CharField(widget=forms.Textarea())
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
