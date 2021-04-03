from django.urls import path
from django.views.generic import TemplateView

from apps.post import views
from apps.post.views import like_unlike_post, PostDeleteView, PostUpdateView, post_list_view, CommentDelete
from apps.profiles.views import followings_list, edit_my_profile_view, followers_list, ProfilesList, \
    accept_follow_request, decline_follow_request, received_requests_view, send_follow_request, unfollow, \
    remove_follower, ProfileDetail, autocomplete_search

app_name = 'posts'

urlpatterns = [
    path('', post_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete_comment/', CommentDelete.as_view(), name='comment-delete'),
    path('<int:pk>/', views.post_detail, name='post-detail-view'),
    path('create_post/', views.create_new_post, name='new_post'),

    # profile urls

    # path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    path('<user>/followings_list/', followings_list, name='followings_list'),
    path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    path('<user>/followers_list/', followers_list, name='followers_list'),
    path('profiles_list/', ProfilesList.as_view(), name='profiles_list'),
    path('follow_requests/', received_requests_view, name='follow_requests'),
    path('<int:request_id>/accept_request/', accept_follow_request, name='accept_request'),
    path('<int:request_id>/decline_request/', decline_follow_request, name='decline_request'),
    path('<email>/send_follow_request/', send_follow_request, name='send_follow_request'),
    path('<following>/unfollow/', unfollow, name='unfollow'),
    path('<follower>/remove_follower/', remove_follower, name='remove_follower'),
    path('search/', autocomplete_search, name='search'),
    path('setting/', TemplateView.as_view(template_name="profiles/setting.html"), name='setting'),


]
