from django.urls import path
from django.views.generic import TemplateView

from apps.profiles.views import followings_list, ProfileDetail, edit_my_profile_view

app_name = 'profiles'

urlpatterns = [
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    path('followings_list/', followings_list, name='followings_list'),
    # path('edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),
    # path('send_follow_request/', send_follow_request, 'send_request'),
    # path('accept_follow_request/',accept_follow_request,'accept_request'),
    # path('requests/', TemplateView.as_view(template_name='profiles/follow_requests.html'), name='requests'),
    # path('search/',SearchView.as_view(),name='search'),
    # path('followers_list/', TemplateView.as_view(template_name='profiles/followers_list.html'), name='followings_list'),
    # path('profile/<first_name>/',TemplateView.as_view(template_name='profiles/profile.html'), name='profile_view'),

]
