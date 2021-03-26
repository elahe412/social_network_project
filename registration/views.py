from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from registration.forms import ProfileCreationForm


class SignupView(FormView):
    """sign up user view"""

    form_class = ProfileCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


def Dashboard(request):
    """ make dashboard view """
    return render(request, 'registration/dashboard.html')


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'registration/dashboard.html')
        else:
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
                    return redirect('dashboard')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'registration/login.html', {'message': message})
