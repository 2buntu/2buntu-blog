from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    """Form for new user registrations."""

    email = forms.EmailField(help_text="Used for verifying your account and password resets.")

class ResetForm(PasswordResetForm):
    """Form for resetting a user's password."""

    email = forms.EmailField(help_text="Email address used when registering.")

    def clean_email(self):
        """Verify that the email address is valid."""
        try:
            return User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise ValidationError("The email address you provided does not match any valid account.")
