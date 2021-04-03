from django.urls import path

from apps.post import views
from apps.post.views import like_unlike_post, PostDeleteView, PostUpdateView, post_list_view, CommentDelete
from apps.profiles.views import followings_list, edit_my_profile_view, followers_list, ProfilesList, \
    accept_follow_request, decline_follow_request, received_requests_view, send_follow_request, unfollow, \
    remove_follower, autocomplete_search

app_name = 'posts'

urlpatterns = [
    path('', post_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete_comment/', CommentDelete.as_view(), name='comment-delete'),
    path('<int:pk>/', views.post_detail, name='post-detail-view'),
    path('create_post/', views.create_new_post, name='new_post'),

    # otp urls
    # path('', login_attempt, name="login"),
    # path('otp', otp, name="otp"),
    # path('login-otp', login_otp, name="login_otp")

]
