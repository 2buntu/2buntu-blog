from django.shortcuts import get_object_or_404, render
from twobuntu.articles.models import Article
from twobuntu.categories.models import Category

def view(request, id, slug):
    """Display articles filed under the specified category."""
    category = get_object_or_404(Category, pk=id)
    return render(request, 'categories/view.html', {
        'title':    category.name,
        'articles': Article.objects.filter(category=category, published=True),
    })
