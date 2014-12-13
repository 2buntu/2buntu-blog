from json import loads
from sys import _getframe

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_bytes, smart_text
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

from twobuntu.captcha.widgets import CaptchaInput


class CaptchaField(forms.Field):
    """
    Field for displaying a captcha widget.
    """

    widget = CaptchaInput

    def __init__(self, theme=None, *args, **kwargs):
        self.theme = theme
        super(CaptchaField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(CaptchaField, self).widget_attrs(widget)
        attrs.update({
            'theme': self.theme,
        })
        return attrs

    # Originally copied from django-recaptcha
    # Released under the BSD license
    # https://pypi.python.org/pypi/django-recaptcha
    def get_remoteip(self):
        f = _getframe()
        while f:
            request = f.f_locals.get('request', None)
            if request:
                return request.META.get(
                    'HTTP_X_FORWARDED_FOR',
                    request.META.get('REMOTE_ADDR', ''),
                )
            f = f.f_back

    def validate(self, value):
        super(CaptchaField, self).validate(value)
        params = urlencode({
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': smart_bytes(value),
            'remoteip': self.get_remoteip(),
        })
        url = 'https://www.google.com/recaptcha/api/siteverify?%s' % params
        if not loads(smart_text(urlopen(url).read())).get('success', False):
            raise ValidationError("Incorrect captcha solution provided.")
        return value
