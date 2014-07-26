from django.shortcuts import render


def index(request):
    """
    Display information about the API.
    """
    return render(request, 'api/index.html', {
        'title': 'API',
    })
