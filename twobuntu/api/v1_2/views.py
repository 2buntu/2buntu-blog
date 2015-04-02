from calendar import timegm
from hashlib import md5
from json import dumps, JSONEncoder, loads

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_bytes, smart_text

from twobuntu.accounts.models import Profile
from twobuntu.articles.models import Article
from twobuntu.categories.models import Category
from twobuntu.utils import timestamp_to_datetime


def index(request):
    """
    Display information about the API.
    """
    return render(request, 'api/v1_2/index.html', {
        'title': 'API',
    })


class APIException(Exception):
    """
    Base for all API exceptions.
    """


class ObjectEncoder(JSONEncoder):
    """
    JSON encoder for supported Django model instances.
    """

    def __init__(self, request, **kwargs):
        """
        Initialize the encoder.
        """
        self._request = request
        super(ObjectEncoder, self).__init__()

    def default(self, o):
        """
        Encode the provided object.
        """
        if type(o) is QuerySet:
            return list(o)
        elif type(o) is Article:
            return self._encode_article(o)
        elif type(o) is Category:
            return self._encode_category(o)
        elif type(o) is Profile:
            return self._encode_profile(o)
        else:
            return JSONEncoder.default(self, o)

    def _encode_article(self, article):
        """
        Encode an article.
        """
        return {
            'id': article.id,
            'title': smart_text(article),
            'author': {
                'id': article.author.id,
                'name': smart_text(article.author.profile),
                'email_hash': md5(smart_bytes(article.author.email)).hexdigest(),
            },
            'category': {
                'id': article.category.id,
                'name': article.category.name,
            },
            'body': article.render(),
            'cc_license': article.cc_license,
            'date': timegm(article.date.utctimetuple()),
            'url': self._request.build_absolute_uri(article.get_absolute_url()),
        }

    def _encode_category(self, category):
        """
        Encode a category.
        """
        return {
            'id': category.id,
            'name': category.name,
            'articles': category.num_articles,
            'url': self._request.build_absolute_uri(category.get_absolute_url()),
        }

    def _encode_profile(self, profile):
        """
        Encode a profile.
        """
        return {
            'id': profile.user.id,
            'name': smart_text(profile),
            'email_hash': md5(smart_bytes(profile.user.email)).hexdigest(),
            'age': profile.age(),
            'location': profile.location,
            'website': profile.website,
            'bio': profile.bio,
            'last_seen': timegm(profile.user.last_login.utctimetuple()) if profile.user.last_login else 0,
            'url': self._request.build_absolute_uri(profile.get_absolute_url()),
        }


def endpoint(fn):
    """
    Wrap the API endpoint.
    """
    def wrap(request, **kwargs):
        try:
            json = dumps(
                fn(request, **kwargs),
                cls=ObjectEncoder,
                request=request,
            )
        except APIException as e:
            json = dumps({
                'error': smart_text(e),
            })
        if 'debug' in request.GET:
            return render(request, 'api/v1_2/debug.html', {
                'title': '2buntu API Debugger',
                'parent': {
                    'title': 'API',
                    'url': reverse('api:index'),
                },
                'json': dumps(loads(json), indent=4),
            })
        elif 'callback' in request.GET:
            return HttpResponse(
                '%s(%s)' % (request.GET['callback'], json),
                content_type='application/javascript; charset=utf-8',
            )
        else:
            return HttpResponse(json, content_type='application/json')
    return wrap


def paginate(fn):
    """
    Limit the number of items returned.
    """
    def wrap(request, **kwargs):
        try:
            page = max(int(request.GET['page']), 1) if 'page' in request.GET else 1
            size = min(max(int(request.GET['size']), 0), 20) if 'size' in request.GET else 20
        except ValueError:
            raise APIException("Invalid page and/or size parameter specified.")
        return fn(request, **kwargs)[(page - 1) * size:page * size]
    return wrap


def minmax(field):
    """
    Process minimum and maximum parameters.
    """
    def outer(fn):
        def inner(request, **kwargs):
            filters = {}
            try:
                if 'min' in request.GET:
                    filters['%s__gte' % field] = timestamp_to_datetime(int(request.GET['min']))
                if 'max' in request.GET:
                    filters['%s__lte' % field] = timestamp_to_datetime(int(request.GET['max']))
            except ValueError:
                raise APIException("Invalid min and/or max parameter specified.")
            return fn(request, **kwargs).filter(**filters)
        return inner
    return outer


@endpoint
@paginate
@minmax('date')
def articles(request):
    """
    Return all recent articles.
    """
    return Article.objects.select_related('author', 'author__profile', 'category').filter(status=Article.PUBLISHED)


@endpoint
def article_by_id(request, id):
    """
    Return the specified article.
    """
    return Article.objects.select_related('author', 'author__profile', 'category').filter(pk=id, status=Article.PUBLISHED)


@endpoint
@paginate
@minmax('user__last_login')
def authors(request):
    """
    Return most popular authors.
    """
    return Profile.objects.select_related('user').all()


@endpoint
def author_by_id(request, id):
    """
    Return the specified author.
    """
    return Profile.objects.select_related('user').filter(pk=id)


@endpoint
@paginate
@minmax('date')
def articles_by_author(request, id):
    """
    Return articles written by the specified author.
    """
    return Article.objects.select_related('author', 'author__profile', 'category').filter(author=id, status=Article.PUBLISHED)


@endpoint
@paginate
def categories(request):
    """
    Return most popular categories.
    """
    return Category.objects.all().annotate(num_articles=Count('article'))


@endpoint
@paginate
@minmax('date')
def articles_by_category(request, id):
    """
    Return recent articles in the specified category.
    """
    return Article.objects.select_related('author', 'author__profile', 'category').filter(category=id, status=Article.PUBLISHED)
