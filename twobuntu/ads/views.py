from django.shortcuts import render


def index(request):
    """
    Display advertising information.
    """
    return render(request, 'ads/index.html', {
        'title': 'Advertising',
    })
