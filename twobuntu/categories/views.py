from django.shortcuts import render

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category
from twobuntu.decorators import canonical


@canonical(Category)
def view(request, category):
    """
    Display articles filed under the specified category.
    """
    return render(request, 'categories/view.html', {
        'title': category.name,
        'category': category,
        'articles': Article.objects.select_related('author','author__profile','category').filter(category=category, status=Article.PUBLISHED),
    })
