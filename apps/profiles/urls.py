
from django.urls import path
from django.views.generic import TemplateView

from apps.profiles.views import edit_my_profile_view, ProfileDetail,followings_list
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    path('followings_list/', followings_list, name='followings_list'),

    # path('profile/<first_name>/',TemplateView.as_view(template_name='profiles/profile.html'), name='profile_view'),

    ]

