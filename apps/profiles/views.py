from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile


# class ProfileUpdateView(UpdateView):
#     form_class = ProfileModelForm
#     model = Profile
#     template_name = 'profiles/edit_profile.html'
#     success_url = reverse_lazy('posts:profile-detail-view')
#
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save()
#             return super().form_valid(form)


@login_required
def edit_my_profile_view(request):
    obj = Profile.objects.get(email=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {'obj': obj, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/edit_profile.html', context)

class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profiles/profile_details.html'


def followings_list(request):
    user = Profile.objects.get(email=request.user)
    context = {'user': user}
    return render(request, 'profiles/followings_list.html', context)


# @login_required()
# def send_follow_request(request, user_id):
#     follower = request.user
#     following = Profile.objects.get(email=user_id)
#     follow_request, created = FollowRequest.objects.get_or_create(follower=follower, following=following)
#     if created:
#         follow_request.status = 'send'
#         follow_request.save()
#         return HttpResponse("request send")
#     else:
#         return HttpResponse("request was already sent")


# @login_required()
# def accept_follow_request(request, request_id):
#     follow_request = FollowRequest.objects.get(id=request_id)
#     if follow_request.following == request.user:
#         follow_request.following.follower.add(follow_request.follower)
#         follow_request.follower.following.add(follow_request.following)
#         follow_request.status = 'accepted'
#         follow_request.save()
#         return HttpResponse('follow request accepted')
#     else:
#         follow_request.status = 'rejected'
#         follow_request.save()
#         return HttpResponse('request not accepted')


# @login_required()
# def decline_follow_request(request):
#     if request.method=="POST":
#         pk = request.POST.get('profile_pk')
#         receiver = Profile.objects.get(user=request.user)
#         sender = Profile.objects.get(pk=pk)
#         rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
#         rel.delete()
#     return redirect('profiles:my-invites-view')
#
#
# def reject_invatation(request):
#     if request.method=="POST":
#         pk = request.POST.get('profile_pk')
#         receiver = Profile.objects.get(user=request.user)
#         sender = Profile.objects.get(pk=pk)
#         rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
#         rel.delete()
#     return redirect('profiles:my-invites-view')

class SearchView(ListView):
    model = Profile
    template_name = 'profiles/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Profile.objects.filter(email__icontains=query)
        return object_list
