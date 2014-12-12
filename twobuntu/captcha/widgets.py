from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class CaptchaInput(forms.Widget):
    """
    Widget for human verification.
    """

    def render(self, name, value, attrs=None):
        return mark_safe(render_to_string('captcha/widget.html', {
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'theme': attrs.get('theme', 'light'),
        }))

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response', None)
