from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    """Form for new user registrations."""

    email = forms.EmailField(help_text="Used for verifying your account and password resets.")
