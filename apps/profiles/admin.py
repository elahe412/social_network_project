from django.contrib import admin

from apps.profiles.models import Profile, FollowRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['email', 'first_name', 'last_name', 'created']


@admin.register(FollowRequest)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'status']
