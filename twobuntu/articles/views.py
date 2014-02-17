from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from twobuntu.articles.models import Article

def view(request, id, slug):
    """Display the specified article."""
    article = get_object_or_404(Article, pk=id, published=True)
    return render(request, 'articles/view.html', {
        'title':   article.title,
        'parent':  {
            'title': article.category,
            'url':   article.category.get_absolute_url(),
        },
        'article': article,
    })

def search(request):
    """Display search results."""
    if not 'q' in request.GET:
        return redirect('home')
    q = request.GET['q']
    return render(request, 'articles/search.html', {
        'title':    'Search Results for "%s"' % q,
        'articles': Article.objects.filter(published=True).filter(Q(title__icontains=q) | Q(body__icontains=q)),
    })
