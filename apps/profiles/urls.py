
from django.urls import path
from django.views.generic import TemplateView

from apps.profiles.views import edit_my_profile_view
from . import views

app_name = 'profiles'

urlpatterns = [

    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.Dashboard, name='dashboard'),
    path('logout/', views.Logout, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    path('profile/<first_name>/',TemplateView.as_view(template_name='profiles/profile.html'), name='profile_view'),
    # path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    ]

