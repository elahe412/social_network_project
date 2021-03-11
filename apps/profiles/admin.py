from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.profiles.models import Profile, Follow
from common.forms import ProfileCreationForm


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileCreationForm
    list_display = ['email','username', 'first_name', 'last_name', 'created']



@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'status']
