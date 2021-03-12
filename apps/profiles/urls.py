
from django.urls import path

from apps.profiles.views import edit_my_profile_view
from . import views

app_name = 'profiles'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.Dashboard, name='dashboard'),
    path('logout/', views.Logout, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    ]

