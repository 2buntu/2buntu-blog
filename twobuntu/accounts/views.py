from django.contrib import messages
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from twobuntu.accounts.forms import ProfileForm, RegistrationForm, ResetForm
from twobuntu.accounts.models import ConfirmationKey, Profile
from twobuntu.articles.models import Article
from twobuntu.decorators import canonical


@canonical(Profile)
def profile(request, profile):
    """
    Display a user's profile.
    """
    return render(request, 'accounts/profile.html', {
        'title': profile,
        'profile': profile,
        'articles': Article.apply_filter(request, Q(author=profile.user)),
    })


def login(request):
    """
    Log a user in.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'title': 'Login',
        'form': form,
        'action': 'Login',
    })


@login_required
def logout(request):
    """
    Log a user out.
    """
    logout_user(request)
    messages.info(request, "You have successfully been logged out.")
    return redirect('home')


@transaction.atomic
def register(request):
    """
    Present a registration form for new users.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            key = ConfirmationKey(user=user)
            key.save()
            template = render_to_string('accounts/emails/register.txt', {
                'user': user,
                'url': request.build_absolute_uri(reverse('accounts:register_confirm', kwargs={'key': key.key})),
            })
            send_mail('2buntu Registration', template, '2buntu <noreply@2buntu.com>', [user.email])
            messages.info(request, "Please check the email address you provided for instructions on activating your account.")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'form.html', {
        'title': 'Register',
        'form': form,
        'description': "Please fill in the form below to create your account.",
        'action': 'Register',
    })


@transaction.atomic
def register_confirm(request, key):
    """
    Confirms a user account.

    :param key: confirmation key to confirm registration
    """
    key = get_object_or_404(ConfirmationKey, key=key)
    key.user.is_active = True
    key.user.save()
    key.delete()
    messages.info(request, "Thank you! Your account has been activated. Please log in below.")
    return redirect('accounts:login')


def reset(request):
    """
    Prompt a user for their email address.
    """
    if request.method == 'POST':
        form = ResetForm(data=request.POST)
        if form.is_valid():
            key = ConfirmationKey(user=form.user)
            key.save()
            template = render_to_string('accounts/emails/reset.txt', {
                'user': key.user,
                'url': request.build_absolute_uri(reverse('accounts:reset_confirm', kwargs={'key': key.key})),
            })
            send_mail('2buntu Password Reset', template, '2buntu <noreply@2buntu.com>', [key.user.email])
            messages.info(request, "An email has been sent to the address you provided with instructions on completing the password reset procedure.")
            return redirect('home')
    else:
        form = ResetForm()
    return render(request, 'form.html', {
        'title': 'Reset Password',
        'form': form,
        'description': "Please fill in the form below to begin the password reset procedure.",
        'action': 'Continue',
    })


@transaction.atomic
def reset_confirm(request, key):
    """
    Complete the password reset procedure.
    """
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
        'title': 'Set Password',
        'form': form,
        'description': "Please enter a new password for your account.",
        'action': 'Continue',
    })


@login_required
@transaction.atomic
def edit(request, id):
    """
    Update the specified user profile.
    """
    profile = get_object_or_404(Profile, user=id)
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            form.save()
            return redirect(profile)
    else:
        form = ProfileForm(
            instance=profile,
            initial={
                'first_name': profile.user.first_name,
                'last_name': profile.user.last_name,
                'email': profile.user.email,
            })
    return render(request, "form.html", {
        'title': 'Edit Profile',
        'form': form,
        'description': "Use the form below to make changes to this user profile.",
        'action': 'Save',
    })
