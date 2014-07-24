from calendar import timegm
from datetime import datetime
from hashlib import md5
from json import dumps

from django.http import HttpResponse

from twobuntu.articles.models import Article


def endpoint(fn):
    """
    Designate a view as an API endpoint.
    """
    def wrap(request, **kwargs):
        try:
            json = dumps(fn(request, **kwargs))
        except Exception, e:
            json = dumps({
                'error': str(e),
            })
        if 'callback' in request.GET:
            return HttpResponse(
                '%s(%s)' % (request.GET['callback'], json,),
                content_type='application/javascript',
            )
        else:
            return HttpResponse(json, content_type='application/json')
    return wrap


def articles(fn):
    """
    Generate an article dictionary from a function that returns an article list.
    """
    def wrap(request, **kwargs):
        return [{
            'id': a.id,
            'title': a.title,
            'body': a.render(),
            'author': {
                'name': str(a.author.profile),
                'email_hash': md5(a.author.email).hexdigest(),
            },
            'url': request.build_absolute_uri(a.get_absolute_url()),
            'published_date': timegm(a.date.utctimetuple()),
            'modified_date': timegm(a.date.utctimetuple()),
        } for a in fn(request, **kwargs)]
    return wrap


def paginate(fn):
    """
    Limit the number of items returned.
    """
    def wrap(request, **kwargs):
        p = int(request.GET['page']) if 'page' in request.GET else 1
        s = max(int(request.GET['size']), 20) if 'size' in request.GET else 20
        return fn(request, **kwargs)[(p - 1) * s:p * s]
    return wrap


def minmax(fn):
    """
    Process minimum and maximum parameters.
    """
    def wrap(request, **kwargs):
        f = {}
        if 'min' in request.GET:
            f['date__gte'] = datetime.fromtimestamp(int(request.GET['min']))
        if 'max' in request.GET:
            f['date__lte'] = datetime.fromtimestamp(int(request.GET['max']))
        return fn(request, **kwargs).filter(**f)
    return wrap


@endpoint
@articles
@paginate
@minmax
def published(request):
    """Return articles sorted by publication date."""
    return Article.objects.filter(status=Article.PUBLISHED).order_by('-date')


@endpoint
@articles
@paginate
@minmax
def modified(request):
    """Return articles sorted by modification date."""
    return Article.objects.filter(status=Article.PUBLISHED).order_by('-date')


@endpoint
@articles
def article(request, id):
    """Return information about a specific article."""
    return [Article.objects.filter(status=Article.PUBLISHED).get(pk=id)]
