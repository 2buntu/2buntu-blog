from django.contrib import messages
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from twobuntu.accounts.forms import RegistrationForm
from twobuntu.accounts.models import ConfirmationKey
from twobuntu.articles.models import Article

def profile(request, id, slug):
    """Display a user's profile."""
    user = get_object_or_404(User, pk=id)
    return render(request, 'accounts/profile.html', {
        'title':    user.profile,
        'profile':  user.profile,
        'articles': Article.objects.filter(author=user, published=True),
    })

def login(request):
    """Log a user in."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
    else:
        form = AuthenticationForm()
    return render(request, 'form.html', {
        'title':       'Login',
        'form':        form,
        'description': "Please enter your username and password to login.",
        'action':      'Login',
    })

@login_required
def logout(request):
    """Log a user out."""
    logout_user(request)
    messages.info(request, "You have successfully been logged out.")
    return redirect('home')

def register(request):
    """Present a registration form for new users."""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            key = ConfirmationKey(user=user)
            key.save()
            template = render_to_string('emails/register.txt', {
                'username': user.username,
                'url':      request.build_absolute_uri(key.get_absolute_url()),
            })
            send_mail('2buntu Registration', template, '2buntu <noreply@2buntu.com>', [user.email,])
            messages.info(request, "Please check the email address you provided for instructions on activating your account.")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'form.html', {
        'title':       'Register',
        'form':        form,
        'description': "Please fill in the form below to create your account.",
        'action':      'Register'
    })

def confirm(request, key):
    """Confirms a user account."""
    key = get_object_or_404(ConfirmationKey, key=key)
    key.user.is_active = True
    key.user.save()
    messages.info(request, "Thank you! Your account has been activated. Please log in below.")
    return redirect('accounts:login')
