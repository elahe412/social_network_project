"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from registration.views import LoginView, Dashboard, Logout, change_password, SignupView,ActivateView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/',ActivateView.as_view(), name='activate'),
    # path('singup/', usersignup, name='signup'),
    # path('activate/',activate_account, name='activate'),
    path('change_password/', change_password, name='change_password'),
    path('home/', Dashboard, name='dashboard'),
    path('logout/', Logout, name='logout'),
    path('admin/', admin.site.urls),
    path('profiles/', include('apps.profiles.urls', namespace='profiles')),
    path('posts/', include('apps.post.urls', namespace='posts')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
