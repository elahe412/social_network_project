from django.urls import path

from apps.profiles.views import  ProfileDetail, followings_list,ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail-view'),
    path('edit_myprofile/', ProfileUpdateView.as_view(), name='my_profile_view'),
    path('followings_list/', followings_list, name='followings_list'),
    # path('followers_list/', TemplateView.as_view(template_name='profiles/followers_list.html'), name='followings_list'),

    # path('profile/<first_name>/',TemplateView.as_view(template_name='profiles/profile.html'), name='profile_view'),

]
