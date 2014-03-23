from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from twobuntu.articles.forms import EditorForm
from twobuntu.articles.models import Article
from twobuntu.decorators import canonical

@canonical(Article)
def view(request, article):
    """Display the specified article."""
    if not article.can_view(request):
        raise Http404
    return render(request, 'articles/view.html', {
        'title':   article.title,
        'parent':  {
            'title': article.category,
            'url':   article.category.get_absolute_url(),
        },
        'article':  article,
        'can_edit': article.can_edit(request),
        'social': (
            ('https://www.facebook.com/sharer.php?u=',              'Facebook', 'fa-facebook-square',),
            ('https://plus.google.com/share?url=',                  'Google+',  'fa-google-plus-square',),
            ('https://twitter.com/share?url=',                      'Twitter',  'fa-twitter-square',),
            ('http://tumblr.com/share?s=&v=3&u=',                   'Tumblr',   'fa-tumblr-square',),
            ('http://www.linkedin.com/shareArticle?mini=true&url=', 'LinkedIn', 'fa-linkedin-square',),
        ),
    })

def search(request):
    """Display search results."""
    if not 'q' in request.GET:
        return redirect('home')
    q = request.GET['q']
    return render(request, 'articles/search.html', {
        'title':    'Search Results for "%s"' % q,
        'articles': Article.objects.filter(status=Article.PUBLISHED).filter(Q(title__icontains=q) | Q(body__icontains=q)),
    })

@login_required
def editor(request, id):
    """Display the article editor."""
    article = get_object_or_404(Article, pk=id) if id else None
    if article and not article.can_edit(request):
        raise Http404
    if request.method == 'POST':
        form = EditorForm(instance=article, data=request.POST)
        if form.is_valid():
            creating = article is None
            article = form.save(commit=False)
            if creating:
                article.author = request.user
            article.save()
            messages.info(request, "The article has been saved." if creating else "Your changes to the article have been saved.")
            if 'action' in request.POST and request.POST['action'] == 'continue':
                return redirect('articles:editor', article.id)
            else:
                return redirect(article)
    else:
        form = EditorForm(instance=article)
    return render(request, 'articles/editor.html', {
        'title':       'Edit "%s"' % article if article else 'New Article',
        'form':        form,
        'description': "Use the form below to %s." % ('edit the article' if article else 'create an article',),
    })

def markdown(request):
    """Display Markdown help."""
    return render(request, 'articles/markdown.html', {
        'title':  'Markdown Help',
    })

@login_required
def submit(request, id):
    """Submit an article for approval."""
    article = get_object_or_404(Article, pk=id, status=Article.DRAFT)
    article.status = Article.UNAPPROVED
    article.save()
    messages.info(request, "The article has been submitted for approval by a staff member.")
    return redirect(article)

@user_passes_test(lambda u: u.is_staff)
def publish(request, id):
    """Publish the specified article."""
    article = get_object_or_404(Article, pk=id)
    article.status = Article.PUBLISHED
    article.save()
    messages.info(request, "The article has been published.")
    return redirect(article)
