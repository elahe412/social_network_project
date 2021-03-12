from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.profiles.models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = ['email', 'first_name', 'last_name', 'created']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'status']
