from django.urls import path

from apps.profiles.views import followings_list, ProfileDetail, edit_my_profile_view, followers_list, ProfilesList, \
    received_requests_view, accept_follow_request, decline_follow_request

app_name = 'profiles'

urlpatterns = [
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    path('edit_myprofile/', edit_my_profile_view, name='edit_profile_view'),
    path('followings_list/', followings_list, name='followings_list'),
    path('followers_list/', followers_list, name='followers_list'),
    path('profiles_list/', ProfilesList.as_view(), name='profiles_list'),
    path('follow_requests/', received_requests_view, name='follow_requests'),
    path('accept_request/', accept_follow_request, name='accept_request'),
    path('decline_request/',  decline_follow_request, name='decline_request'),

    # path('edit_myprofile/', ProfileUpdateView.as_view(), name='edit_profile_view'),
    # path('send_follow_request/', send_follow_request, 'send_request'),
    # path('accept_follow_request/',accept_follow_request,'accept_request'),
    # path('requests/', TemplateView.as_view(template_name='profiles/follow_requests.html'), name='requests'),
    # path('search/',SearchView.as_view(),name='search'),
    # path('followers_list/', TemplateView.as_view(template_name='profiles/followers_list.html'), name='followings_list'),
    # path('profile/<first_name>/',TemplateView.as_view(template_name='profiles/profile.html'), name='profile_view'),

]
