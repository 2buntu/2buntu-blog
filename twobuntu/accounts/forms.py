from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User

from twobuntu.accounts.models import Profile

class RegistrationForm(UserCreationForm):
    """Form for new user registrations."""

    email = forms.EmailField(help_text="Used for verifying your account and password resets.")

class ResetForm(PasswordResetForm):
    """Form for resetting a user's password."""

    email = forms.EmailField(help_text="Email address used when registering.")

    def clean_email(self):
        """Verify that the email address is valid."""
        try:
            self.user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError("The email address you provided does not match any valid account.")

class ProfileForm(forms.ModelForm):
    """Form for editing a user's profile."""
    
    class Meta:
        model = Profile
        fields = ('birthday', 'location', 'website', 'bio',)
