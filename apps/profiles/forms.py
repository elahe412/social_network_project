from apps.profiles.models import Profile
from django import forms
from django.contrib.auth import get_user_model


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio','website','gender')


class SignupForm(forms.ModelForm):
    """user signup form"""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('email','password',)


class LoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())