from dateutil.parser import parse
from os import path
from platform import python_version
from re import search
from socket import gethostname
from subprocess import CalledProcessError, Popen, PIPE

from django import get_version
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category
from twobuntu.forms import FeedbackForm
from twobuntu.news.models import Item


def index(request):
    """
    Render the home page.
    """
    return render(request, 'pages/index.html', {
        'title': 'Archives' if 'page' in request.GET else None,
        'home': True,
        'articles': Article.objects.select_related('author', 'author__profile', 'category').filter(status=Article.PUBLISHED),
        'categories': Category.objects.filter(article__status=Article.PUBLISHED).annotate(num_articles=Count('article')),
        'items': Item.objects.all(),
        'users': User.objects.select_related('profile').filter(is_active=True).annotate(num_articles=Count('article')).order_by('-num_articles'),
    })


def commit():
    """
    Retrieve the current commit.
    """
    try:
        process = Popen(['git', 'log', '-1'], stdout=PIPE, cwd=path.dirname(__file__))
        output, error = process.communicate()
        return {
            'hash': search(br'commit\s*(.*)', output).group(1)[:8],
            'author': search(br'Author:\s*(.*)<', output).group(1),
            'date': parse(search(br'Date:\s*(.*)', output).group(1)),
        }
    except (AttributeError, CalledProcessError):
        return {}


# Due to memory problems with fork, the git commit information should be
# retrieved only once when the application starts
_commit = commit()


def about(request):
    """
    Render the about page.
    """
    return render(request, 'pages/about.html', {
        'title': 'About Us',
        'num_articles': Article.objects.filter(status=Article.PUBLISHED).count(),
        'num_users': User.objects.filter(is_active=True).count(),
        'hostname': gethostname(),
        'django_version': get_version(),
        'python_version': python_version(),
        'commit': _commit,
    })


def links(request):
    """
    Render the links page.
    """
    return render(request, 'pages/links.html', {
        'title': 'Links',
    })


def feedback(request):
    """
    Gather feedback from users.
    """
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            template = render_to_string('emails/feedback.txt', {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'comments': form.cleaned_data['comments'],
            })
            mail_admins('2buntu Feedback', template)
            messages.info(request, "Thank you for your feedback. Your message was successfully sent to our administrators.")
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, "form.html", {
        'title': "Feedback",
        'form': form,
        'description': "We value your feedback! Please fill in the form below to leave us a note, tip, or suggestion.",
        'action': 'Submit',
    })


def join(request):
    """
    Provide guidelines for joining and contributing to the blog.
    """
    return render(request, 'pages/join.html', {
        'title': 'Join',
    })


def opensearch(request):
    """
    Return OpenSearch XML file.
    """
    return render(request, 'xml/opensearch.xml', {
        'image_url': request.build_absolute_uri(static('img/favicon.png')),
        'search_url': request.build_absolute_uri(reverse('articles:search')),
    }, content_type='text/xml')


def old(request, id):
    """
    Redirect the client to the new URL for old articles.
    """
    return redirect(get_object_or_404(Article, pk=id), permanent=True)
