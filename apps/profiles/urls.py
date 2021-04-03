from django.urls import path

from apps.profiles.views import followings_list, ProfileDetail, edit_my_profile_view, followers_list, ProfilesList, \
    received_requests_view, accept_follow_request, decline_follow_request, send_follow_request, unfollow, \
    remove_follower, autocomplete_search

app_name = 'profiles'

urlpatterns = [
    path('<user>/followings_list/', followings_list, name='followings_list'),
    path('edit_myprofile/', edit_my_profile_view, name='edit_profile_view'),
    path('<user>/followers_list/', followers_list, name='followers_list'),
    path('profiles_list/', ProfilesList.as_view(), name='profiles_list'),
    path('follow_requests/', received_requests_view, name='follow_requests'),
    path('<int:request_id>/accept_request/', accept_follow_request, name='accept_request'),
    path('<int:request_id>/decline_request/', decline_follow_request, name='decline_request'),
    path('<email>/send_follow_request/', send_follow_request, name='send_follow_request'),
    path('<following>/unfollow/', unfollow, name='unfollow'),
    path('<follower>/remove_follower/', remove_follower, name='remove_follower'),
    path('search/', autocomplete_search, name='search'),
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),



]
