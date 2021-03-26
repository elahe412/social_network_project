from django.urls import path
from apps.post import views
from apps.post.views import like_unlike_post, PostDeleteView, PostUpdateView, post_list_view


app_name='posts'

urlpatterns = [
    path('', post_list_view, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/', views.post_detail, name='post-detail-view'),
    path('create_post/', views.create_new_post, name='new_post'),
    # path('edit_myprofile/', edit_my_profile_view, name='my_profile_view'),
    # path('edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),
    # path('<slug>/edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),

    # path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    ]