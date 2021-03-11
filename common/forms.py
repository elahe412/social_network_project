from django.contrib.auth.forms import UserCreationForm

from apps.profiles.models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email']

