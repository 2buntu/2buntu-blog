from django.shortcuts import get_object_or_404, redirect

from twobuntu.shorturls.models import ShortURL


def shorturl(request, key):
    """
    Redirect the client.
    """
    return redirect(get_object_or_404(ShortURL, pk=key).url)
