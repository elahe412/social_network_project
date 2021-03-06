from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.profiles.models import Profile


class ProfileCreationForm(UserCreationForm):
    """
    creating profile object that is a user of django user model
    """
    class Meta:
        model = Profile
        fields = ('email',)


class LoginForm(forms.Form):
    """
    user login form
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
