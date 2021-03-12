from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages


class SignupView(FormView):
    """sign up user view"""
    form_class = forms.SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profiles:dashboard')

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
    return render(request,'registration/dashboard.html')


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('profiles:dashboard'))


class LoginView(FormView):
    """login view"""

    form_class = forms.LoginForm
    success_url = reverse_lazy('profiles:dashboard')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('profiles:login'))


def edit_my_profile_view(request):
    obj = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {'obj': obj, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/myprofile.html', context)
