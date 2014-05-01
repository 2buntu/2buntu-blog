from datetime import datetime
from json import dumps, JSONEncoder

from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpResponse

from twobuntu.accounts.models import Profile
from twobuntu.articles.models import Article
from twobuntu.categories.models import Category

class APIException(Exception):
    """Base for all API exceptions."""

class ObjectEncoder(JSONEncoder):
    """JSON encoder for supported Django model instances."""

    def default(self, o):
        if type(o) is QuerySet:
            return list(o)
        elif type(o) is Article:
            return {
                'title': o.title,
            }
        elif type(o) is Category:
            return {
                'name':  str(o),
                'count': o.num_articles,
            }
        elif type(o) is Profile:
            return {
                'name': str(o),
            }
        else:
            return JSONEncoder.default(self, o)

def endpoint(fn):
    """Wrap the API endpoint."""
    def wrapper(request, **kwargs):
        try:
            json = dumps(fn(request, **kwargs), cls=ObjectEncoder)
        except APIException as e:
            json = dumps({
                'error': str(e),
            })
        if 'callback' in request.GET:
            return HttpResponse('%s(%s)' % (request.GET['callback'], json,),
                                content_type='application/javascript')
        else:
            return HttpResponse(json, content_type='application/json')
    return wrapper

def paginate(fn):
    """Limit the number of items returned."""
    def wrapper(request, **kwargs):
        try:
            page = int(request.GET['page']) if 'page' in request.GET else 1
            size = max(int(request.GET['size']), 20) if 'size' in request.GET else 20
        except ValueError:
            raise APIException("Invalid page and/or size parameter specified.")
        return fn(request, **kwargs)[(page - 1) * size:page * size]
    return wrapper

def minmax(fn):
    """Process minimum and maximum parameters."""
    def wrapper(request, **kwargs):
        filters = {}
        try:
            if 'min' in request.GET:
                filters['date__gte'] = datetime.fromtimestamp(int(request.GET['min']))
            if 'max' in request.GET:
                filters['date__lte'] = datetime.fromtimestamp(int(request.GET['max']))
        except ValueError:
            raise APIException("Invalid min and/or max parameter specified.")
        return fn(request, **kwargs).filter(**filters)
    return wrapper

@endpoint
@paginate
@minmax
def articles(request):
    """Return all recent articles."""
    return Article.objects.filter(status=Article.PUBLISHED)

@endpoint
@paginate
@minmax
def article_by_id(request, id):
    """Return the specified article."""
    return Article.objects.filter(pk=id, status=Article.PUBLISHED)

@endpoint
@paginate
@minmax
def authors(request):
    """Return most popular authors."""
    return Profile.objects.all()

@endpoint
@paginate
@minmax
def author_by_id(request, id):
    """Return the specified author."""
    return Profile.objects.filter(pk=id)

@endpoint
@paginate
@minmax
def articles_by_author(request, id):
    """Return articles written by the specified author."""
    return Article.objects.filter(author__profile=id, status=Article.PUBLISHED)

@endpoint
@paginate
@minmax
def categories(request):
    """Return most popular categories."""
    return Category.objects.all().annotate(num_articles=Count('article'))

@endpoint
@paginate
@minmax
def articles_by_category(request, id):
    """Return recent articles in the specified category."""
    return Article.objects.filter(category=id, status=Article.PUBLISHED)
