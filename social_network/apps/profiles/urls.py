from django.urls import path

from apps.profiles.views import edit_my_profile_view

app_name = 'profiles'

urlpatterns = [
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    ]
