from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(email__iexact=self.request.user)
        sent_request = FollowRequest.objects.filter(follower=profile)
        received_request = FollowRequest.objects.filter(following=profile)
        sent_requests = []
        received_requests = []
        for item in received_request:
            received_requests.append(item.follower.email)
        for item in sent_request:
            sent_requests.append(item.following.email)
        context["sent_requests"] = sent_requests
        context["received_requests"] = received_requests
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


class ProfilesList(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'profiles_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(email__iexact=self.request.user)
        sent_request = FollowRequest.objects.filter(follower=profile)
        received_request = FollowRequest.objects.filter(following=profile)
        sent_requests = []
        received_requests = []
        for item in received_request:
            received_requests.append(item.follower.email)
        for item in sent_request:
            sent_requests.append(item.following.email)
        context["sent_requests"] = sent_requests
        context["received_requests"] = received_requests
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


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


@login_required
def received_requests_view(request):
    profile = Profile.objects.get(email=request.user)
    qs = FollowRequest.objects.requests_received(profile)
    # results = list(map(lambda x: x.follower, qs))
    is_empty = False
    if len(qs) == 0:
        is_empty = True

    context = {
        'requests': qs,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_requests.html', context)


@login_required()
def send_follow_request(request, email):
    follower = request.user
    following = Profile.objects.get(email=email)
    follow_request, created = FollowRequest.objects.get_or_create(follower=follower, following=following)
    if created:
        follow_request.status = 'send'
        follow_request.save()
        return HttpResponse("request send")


@login_required()
def accept_follow_request(request, request_id):
    follow_request = FollowRequest.objects.get(id=request_id)
    if request.method == "POST":
        follow_request.following.follower.add(follow_request.follower)
        follow_request.follower.following.add(follow_request.following)
        # follow_request.status = 'accepted'
        # follow_request.save()
        follow_request.delete()
        return redirect('posts:follow_requests')


@login_required()
def decline_follow_request(request, request_id):
    follow_request = FollowRequest.objects.get(id=request_id)
    if request.method == "POST":
        follow_request.delete()
    return redirect('posts:follow_requests')


def unfollow(request, following_id):
    profile = Profile.objects.get(email=request.user)
    if request.method == "POST":
        following = Profile.objects.get(id=following_id)
        profile.get_followings.remove(following.email)
        following.objects.get_followers.remove(profile.email)
        return HttpResponse('profile unfollowed')


def remove_follower(request, follower):
    profile = Profile.objects.get(email=request.user)
    if request.method == "POST":
        follower = Profile.objects.get(email=follower)
        profile.get_followers.remove(follower.email)
        follower.objects.get_followings.remove(profile.email)
        return HttpResponse('profile unfollowed')

# class SearchView(ListView):
#     model = Profile
#     template_name = 'profiles/search.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Profile.objects.filter(email__icontains=query)
#         return object_list
