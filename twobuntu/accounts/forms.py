from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User

from twobuntu.accounts.models import Profile
from twobuntu.captcha.fields import CaptchaField


class RegistrationForm(UserCreationForm):
    """
    Form for new user registrations.
    """

    email = forms.EmailField(help_text="Used for account verification and password resets.")
    captcha = CaptchaField()


class ResetForm(PasswordResetForm):
    """
    Form for resetting a user's password.
    """

    email = forms.EmailField(help_text="Email address used when registering.")

    def clean_email(self):
        """
        Verify that the email address is valid.
        """
        try:
            self.user = User.objects.get(email=self.cleaned_data['email'], is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError("The email address provided does not match an active account.")


class ProfileForm(forms.ModelForm):
    """
    Form for editing a user's profile.
    """

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="First name [optional].",
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Last name [optional].",
    )
    email = forms.EmailField(help_text="Used for account verification and password resets.")

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'birthday', 'location', 'website', 'bio')
