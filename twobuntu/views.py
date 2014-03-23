from dateutil.parser import parse
from os import path
from re import search
from subprocess import CalledProcessError, Popen, PIPE

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models import Count
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from twobuntu.articles.models import Article
from twobuntu.categories.models import Category
from twobuntu.forms import FeedbackForm
from twobuntu.news.models import Item

def index(request):
    """Render the home page."""
    return render(request, 'pages/index.html', {
        'home':       True,
        'articles':   Article.apply_filter(request),
        'categories': Category.objects.annotate(num_articles=Count('article')),
        'items':      Item.objects.all(),
        'users':      User.objects.filter(is_active=True).annotate(num_articles=Count('article')).order_by('-num_articles'),
    })

def about(request):
    """Render the about page."""
    try:
        process = Popen(['git', 'log', '-1'], stdout=PIPE, cwd=path.dirname(__file__))
        output, error = process.communicate()
        commit = {
            'hash':   search(r'commit\s*(.*)', output).group(1)[:8],
            'author': search(r'Author:\s*(.*)<', output).group(1),
            'date':   parse(search(r'Date:\s*(.*)', output).group(1)),
        }
    except (AttributeError, CalledProcessError):
        commit = {}
    return render(request, 'pages/about.html', {
        'title':        'About Us',
        'num_articles': Article.objects.count(),
        'num_users':    User.objects.count(),
        'commit':       commit,
    })

def links(request):
    """Render the links page."""
    return render(request, 'pages/links.html', {
        'title': 'Links',
    })

def feedback(request):
    """Gathers feedback from users."""
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            template = render_to_string('emails/feedback.txt', form)
            mail_admins('2buntu Feedback', template)
            messages.info(request, "Thank you for your feedback. Your message was successfully sent to our administrators.")
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, "form.html", {
        'title':       "Feedback",
        'form':        FeedbackForm(),
        'description': "We value your feedback! Please fill in the form below to leave us a note, tip, or suggestion.",
        'action':      'Submit',
    })
