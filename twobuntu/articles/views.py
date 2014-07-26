from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import mail_admins
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from twobuntu.articles.forms import EditorForm, ScheduledArticleForm
from twobuntu.articles.models import Article, ScheduledArticle
from twobuntu.decorators import canonical


@canonical(Article)
def view(request, article):
    """
    Display the specified article.
    """
    if not article.can_view(request):
        raise Http404
    return render(request, 'articles/view.html', {
        'title': article.title,
        'parent': {
            'title': article.category,
            'url': article.category.get_absolute_url(),
        },
        'article': article,
        'can_edit': article.can_edit(request),
        'social': (
            ('https://www.facebook.com/sharer.php?u=', 'Facebook', 'fa-facebook-square'),
            ('https://plus.google.com/share?url=', 'Google+', 'fa-google-plus-square'),
            ('https://twitter.com/share?url=', 'Twitter', 'fa-twitter-square'),
            ('http://tumblr.com/share?s=&v=3&u=', 'Tumblr', 'fa-tumblr-square'),
            ('http://www.linkedin.com/shareArticle?mini=true&url=', 'LinkedIn', 'fa-linkedin-square'),
        ),
    })


def search(request):
    """
    Display search results.
    """
    if not 'q' in request.GET:
        raise Http404
    q = request.GET['q']
    return render(request, 'articles/search.html', {
        'title': 'Search Results for "%s"' % q,
        'articles': Article.apply_filter(
            request,
            Q(title__icontains=q) | Q(body__icontains=q)
        ).select_related('author', 'author__profile', 'category'),
    })


@login_required
def editor(request, id):
    """
    Display the article editor.
    """
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
            messages.info(
                request,
                "The article has been saved." if creating else "Your changes to the article have been saved."
            )
            if 'action' in request.POST and request.POST['action'] == 'continue':
                return redirect('articles:editor', article.id)
            else:
                return redirect(article)
    else:
        form = EditorForm(instance=article)
    return render(request, 'articles/editor.html', {
        'title': 'Edit "%s"' % article if article else 'New Article',
        'form': form,
        'description': "Use the form below to %s." % ('edit the article' if article else 'create an article',),
    })


def markdown(request):
    """
    Display Markdown help.
    """
    return render(request, 'articles/markdown.html', {
        'title': 'Markdown Help',
    })


@require_POST
@login_required
@transaction.atomic
def submit(request, id):
    """
    Submit an article for approval.
    """
    article = get_object_or_404(Article, pk=id, author=request.user, status=Article.DRAFT)
    article.status = Article.UNAPPROVED
    article.save()
    template = render_to_string('emails/submit.txt', {
        'article': request.build_absolute_uri(article.get_absolute_url()),
    })
    mail_admins('2buntu Article Submitted', template)
    messages.info(request, "The article has been submitted for approval by a staff member.")
    return redirect(article)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def publish(request, id):
    """
    Publish the specified article.
    """
    article = get_object_or_404(Article, pk=id)
    article.status = Article.PUBLISHED
    article.save()
    messages.info(request, "The article has been published.")
    return redirect(article)


@require_POST
@login_required
def release(request, id):
    """
    Release an article under a CC license.
    """
    article = get_object_or_404(Article, pk=id, author=request.user, cc_license=False)
    article.cc_license = True
    article.save()
    messages.info(request, "The article is now available under a CC BY-SA 4.0 license.")
    return redirect(article)


@user_passes_test(lambda u: u.is_staff)
def schedule(request, id):
    """
    Schedule an article for publishing in the future.
    """
    article = get_object_or_404(Article, ~Q(status=Article.PUBLISHED), pk=id)
    try:
        scheduled_article = article.scheduledarticle
    except ScheduledArticle.DoesNotExist:
        scheduled_article = None
    if request.method == 'POST':
        form = ScheduledArticleForm(instance=scheduled_article, data=request.POST)
        if form.is_valid():
            scheduled_article = form.save(commit=False)
            scheduled_article.article = article
            scheduled_article.save()
            messages.info(request, "The article has been scheduled for publishing.")
            return redirect(article)
    else:
        form = ScheduledArticleForm(instance=scheduled_article)
    return render(request, 'form.html', {
        'title': 'Schedule "%s"' % article.title,
        'parent': {
            'title': article,
            'url': article.get_absolute_url(),
        },
        'description': "Select a date and time to publish the article.",
        'form': form,
        'action': 'Schedule',
    })
