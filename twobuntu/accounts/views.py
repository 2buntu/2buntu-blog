from django.contrib import messages
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from twobuntu.accounts.forms import RegistrationForm, ResetForm
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
    return render(request, 'accounts/login.html', {
        'title':  'Login',
        'form':   form,
        'action': 'Login',
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
                'user': user,
                'url':  request.build_absolute_uri(reverse('accounts:register_confirm', kwargs={'key': key.key,})),
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

def register_confirm(request, key):
    """Confirms a user account."""
    key = get_object_or_404(ConfirmationKey, key=key)
    key.user.is_active = True
    key.user.save()
    key.delete()
    messages.info(request, "Thank you! Your account has been activated. Please log in below.")
    return redirect('accounts:login')

def reset(request):
    """Prompt a user for their email address."""
    if request.method == 'POST':
        form = ResetForm(data=request.POST)
        if form.is_valid():
            key = ConfirmationKey(user=form.user)
            key.save()
            template = render_to_string('emails/reset.txt', {
                'user': key.user,
                'url':  request.build_absolute_uri(reverse('accounts:reset_confirm', kwargs={'key': key.key,})),
            })
            send_mail('2buntu Password Reset', template, '2buntu <noreply@2buntu.com>', [key.user.email,])
            messages.info(request, "An email has been sent to the address you provided with instructions on completing the password reset procedure.")
            return redirect('home')
    else:
        form = ResetForm()
    return render(request, 'form.html', {
        'title':       'Reset Password',
        'form':        form,
        'description': "Please fill in the form below to begin the password reset procedure.",
        'action':      'Continue',
    })

def reset_confirm(request, key):
    """Complete the password reset procedure."""
    key = get_object_or_404(ConfirmationKey, key=key)
    if request.method == 'POST':
        form = SetPasswordForm(user=key.user, data=request.POST)
        if form.is_valid():
            form.save()
            key.delete()
            messages.info(request, "Thank you! Your password has been reset. Please log in below.")
            return redirect('accounts:login')
    else:
        form = SetPasswordForm(user=key.user)
    return render(request, 'form.html', {
        'title':       'Set Password',
        'form':        form,
        'description': "Please enter a new password for your account.",
        'action':      'Continue',
    })
