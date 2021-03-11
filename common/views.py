from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from common.forms import ProfileCreationForm


class RegisterUser(CreateView):
    form_class = ProfileCreationForm
    success_url = 'main-post-view'
    template_name = 'registration/register_user.html'

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        message = ''
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_logout = request.POST.get("logout")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    message = 'Login was successful!'
                    login(request, user)
                    return redirect('posts:main-post-view')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'registration/login.html', {'message': message})



@login_required()
def logout_user(request):
    logout(request)
    return redirect('login')
