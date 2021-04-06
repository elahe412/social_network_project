from django import forms

from apps.profiles.models import Profile


class ProfileModelForm(forms.ModelForm):
    # a form for Profile model to create and update profile
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'website', 'gender', 'avatar')

