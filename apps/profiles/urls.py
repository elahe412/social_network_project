
from django.urls import path

from apps.profiles.views import edit_my_profile_view
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name="home"),
    path('sign_up/', views.sign_up, name="sign-up"),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    ]
