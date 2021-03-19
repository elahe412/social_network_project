from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile


class ProfileUpdateView(UpdateView):
    form_class = ProfileModelForm
    model = Profile
    template_name = 'profiles/edit_profile.html'
    success_url = reverse_lazy('profiles:profile-detail-view')

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)




# @login_required
# def edit_my_profile_view(request):
#     obj = Profile.objects.get(email=request.user)
#     form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
#     confirm = False
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             confirm = True
#     context = {'obj': obj, 'form': form, 'confirm': confirm}
#     return render(request, 'profiles/edit_profile.html', context)


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profiles/profile_details.html'


def followings_list(request):
    user = Profile.objects.get(email=request.user)
    context = {'user': user}
    return render(request, 'profiles/followings_list.html', context)

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
