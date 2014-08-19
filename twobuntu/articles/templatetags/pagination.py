from django import template
from django.core.paginator import Paginator
from django.http import Http404
from django.utils.http import urlencode

register = template.Library()


@register.assignment_tag(takes_context=True)
def paginate(context, items):
    """
    Paginates the provided items.
    """
    try:
        num = int(context['request'].GET['page']) if 'page' in context['request'].GET else 1
        return Paginator(items, 12).page(num)
    except:
        raise Http404


@register.simple_tag(takes_context=True)
def modify_query_string(context, **kwargs):
    """
    Returns the current URL with modified query string.
    """
    qs = dict([(k, v) for k, v in context['request'].GET.items()])
    qs.update(kwargs)
    if 'page' in qs and qs['page'] == 1:
        del qs['page']
    return '%s%s%s' % (
        context['request'].path,
        '?' if qs else '',
        urlencode(qs),
    )
