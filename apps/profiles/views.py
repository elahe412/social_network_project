from django import views
from django.views import View
from django.views.generic import DetailView

from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from apps.profiles.forms import ProfileCreationForm


class SignupView(FormView):
    """sign up user view"""
    form_class = ProfileCreationForm
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
                    return redirect('profiles:dashboard')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'registration/login.html', {'message': message})


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



# class ProfileDetail(DetailView):
#     model = Profile
#     template_name ='profiles/profile_details.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['posts'] = self.get_object().get_all_authors_posts()
#     #     return context
#
#
# class FollowRequests(views.View):
#     rel_r = Follow.objects.filter(follower=profile)
#     rel_s = Relationship.objects.filter(receiver=profile)
#     rel_receiver = []
#     rel_sender = []
#     for item in rel_r:
#         rel_receiver.append(item.receiver.user)
#     for item in rel_s:
#         rel_sender.append(item.sender.user)
#     context["rel_receiver"] = rel_receiver
#     context["rel_sender"] = rel_sender