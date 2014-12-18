from django.conf import settings


def read_only(request):
    """
    Add a template variable indicating read-only mode.
    """
    return {'READ_ONLY': getattr(settings, 'READ_ONLY', False)}
