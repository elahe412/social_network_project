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
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

from common import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.profiles.urls', namespace='profiles')),
    path('posts/', include('apps.post.urls', namespace='posts')),
    ]
    # path('signup/', views.SignupView.as_view(), name='signup'),
    # path('logout/', views.logout, name='logout'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('home/',TemplateView.as_view(template_name='index.html'), name='home'),


