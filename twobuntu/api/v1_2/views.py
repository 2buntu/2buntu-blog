from django.http import HttpResponse

def endpoint(fn):
    """Wrap the API endpoint."""
    def wrapper(request, *args, **kwargs):
        return HttpResponse("This API is currently under development.")
    return wrapper

@endpoint
def articles():
    """Return all recent articles."""

@endpoint
def article_by_id(id):
    """Return the specified article."""

@endpoint
def authors():
    """Return most popular authors."""

@endpoint
def author_by_id(id):
    """Return the specified author."""

@endpoint
def articles_by_author(id):
    """Return articles written by the specified author."""

@endpoint
def categories():
    """Return most popular categories."""

@endpoint
def articles_by_category(id):
    """Return recent articles in the specified category."""
