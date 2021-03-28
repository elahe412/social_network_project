from django.urls import path
from apps.post import views
from apps.post.views import like_unlike_post, PostDeleteView, PostUpdateView, post_list_view
from apps.profiles.views import followings_list, edit_my_profile_view, followers_list, ProfilesList, \
    requests_received_view, accept_follow_request, decline_follow_request

app_name='posts'

urlpatterns = [
    path('', post_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/', views.post_detail, name='post-detail-view'),
    path('create_post/', views.create_new_post, name='new_post'),
    path('followings_list/', followings_list, name='followings_list'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    path('followers_list/', followers_list, name='followers_list'),
    path('profiles_list/',ProfilesList.as_view(), name='profiles_list'),
    path('follow_requests/', requests_received_view, name='follow_requests'),
    path('<int:request_id>/accept_request/', accept_follow_request, name='accept_request'),
    path('<int:request_id>/decline_request/', decline_follow_request, name='decline_request'),



    # path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    # path('edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),
    # path('<slug>/edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),

    # path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    ]