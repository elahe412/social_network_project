from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile, FollowRequest


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = Profile.objects.get(email__iexact=self.request.user)
    #     profile = Profile.objects.get(email=self.request.user)
    #     flw_r = FollowRequest.objects.filter(follower=profile)
    #     flw_s = FollowRequest.objects.filter(following=profile)
    #     rel_receiver = []
    #     rel_sender = []
    #     for item in rel_r:
    #         rel_receiver.append(item.receiver.user)
    #     for item in rel_s:
    #         rel_sender.append(item.sender.user)
    #     context["rel_receiver"] = rel_receiver
    #     context["rel_sender"] = rel_sender
    #     context['posts'] = self.get_object().get_all_authors_posts()
    #     context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
    #     return context

class ProfilesList(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'profiles_list'
    paginate_by = 3

def followings_list(request):
    user = Profile.objects.get(email=request.user)
    followings_list = user.get_followings()

    page = request.GET.get('page', 1)

    paginator = Paginator(followings_list, 2)
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except EmptyPage:
        followings = paginator.page(paginator.num_pages)

    context = {'followings': followings}

    return render(request, 'profiles/followings_list.html', context)


def followers_list(request):
    user = Profile.objects.get(email=request.user)
    followers_list = user.get_followers()

    page = request.GET.get('page', 1)
    paginator = Paginator(followers_list, 2)

    try:
        followers = paginator.page(page)
    except PageNotAnInteger:
        followers = paginator.page(1)
    except EmptyPage:
        followers = paginator.page(paginator.num_pages)

    context = {'followers': followers}

    return render(request, 'profiles/followers_list.html', context)


@login_required()
def send_follow_request(request, user_id):
    follower = request.user
    following = Profile.objects.get(email=user_id)
    follow_request, created = FollowRequest.objects.get_or_create(follower=follower, following=following)
    if created:
        follow_request.status = 'send'
        follow_request.save()
        return HttpResponse("request send")
    else:
        return HttpResponse("request was already sent")


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

# class SearchView(ListView):
#     model = Profile
#     template_name = 'profiles/search.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Profile.objects.filter(email__icontains=query)
#         return object_list
