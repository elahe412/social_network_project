# from django.contrib.auth.forms import UserCreationForm
#
# from apps.profiles.models import Profile
#
#
# class ProfileCreationForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['email']
#

# from django import forms
# from django.contrib.auth import get_user_model


# class SignupForm(forms.ModelForm):
#     """user signup form"""
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password',)
#
#
# class LoginForm(forms.Form):
#     """user login form"""
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())