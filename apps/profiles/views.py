import random

# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile, FollowRequest
# import http.client



# class ProfileUpdateView(UpdateView):
#     form_class = ProfileModelForm
#     model = Profile
#     template_name = 'profiles/edit_profile.html'
#     success_url = reverse_lazy('profiles:profile-detail-view')
#
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save()
#             return super().form_valid(form)


@login_required
def edit_my_profile_view(request):
    """
    edit and update profile by ProfileModelForm
    :param request:
    :return: render of request,context and edit_profile.html
    """
    obj = Profile.objects.get(email=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # to show success message in html file
            confirm = True
    context = {'obj': obj, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/edit_profile.html', context)


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(email__iexact=self.request.user)
        sent_request = FollowRequest.objects.filter(follower=profile).filter(status='send')
        received_request = FollowRequest.objects.filter(following=profile).filter(status='send')
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


class ProfilesList(LoginRequiredMixin, ListView):
    """
    view for show list of all profiles
    """
    model = Profile
    template_name = 'profiles/profiles_list.html'
    # context name use in html file
    context_object_name = 'profiles_list'
    paginate_by = 3


@login_required()
def followings_list(request, user):
    """
    show list of followers of user
    :param request:
    :param user: user that her/his profile is shown
    :return: render of request,context with pagination and followings_list.html
    """
    user = Profile.objects.get(slug=user)
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

@login_required()
def followers_list(request, user):
    """
    show list of followers of user
    :param request:
    :param user: slug of user that her/his profile is shown
    :return: render of request,context with pagination and followers_list.html
    """
    # profile object of user
    user = Profile.objects.get(slug=user)
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
    """
    show follow requests that user received (follow request's following == request.user)
    :param request:
    :return: a html file contain list of requests for user
    """
    profile = Profile.objects.get(email=request.user)
    qs = FollowRequest.objects.requests_received(profile)
    is_empty = False
    if len(qs) == 0:
        is_empty = True

    sent_requests=FollowRequest.objects.filter(follower=profile.id).filter(status='accepted').order_by('-updated')[:2]




    context = {
        'sent_requests':sent_requests,
        'requests': qs,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_requests.html', context)


@login_required()
def send_follow_request(request, email):
    """
    create an object of FollowRequest model and send request to other profiles
    :param request:
    :param email: slug of profile that user is sending request to him/her
    :return: redirect to profile-detail-view url of following profile
    """
    follower = request.user
    following = Profile.objects.get(slug=email)
    follow_request, created = FollowRequest.objects.get_or_create(follower=follower, following=following)
    if created:
        follow_request.status = 'send'
        follow_request.save()

        return redirect('profiles:profile-detail-view', email)


@login_required()
def accept_follow_request(request, request_id):
    """
    by accepting follow request follower will added to followers of following profile
    and following will added to followings of follower profile ,then request object will be deleted
    :param request
    :param request_id
    :return: redirect to follow_requests url
    """
    follow_request = FollowRequest.objects.get(id=request_id)
    if request.method == "POST":
        follow_request.following.follower.add(follow_request.follower)
        follow_request.follower.following.add(follow_request.following)
        follow_request.status = 'accepted'
        follow_request.save()
        # follow_request.delete()
        return redirect('profiles:follow_requests')


@login_required()
def decline_follow_request(request, request_id):
    """
    by decline follow request request object will be deleted and user not allow that profile to follow him/her
    :param request_id
    :return: redirect to follow_requests url :
    """
    follow_request = FollowRequest.objects.get(id=request_id)
    if request.method == "POST":
        follow_request.delete()
    return redirect('profiles:follow_requests')


@login_required()
def unfollow(request, following):
    """
    if user follow someone else he/she can unfollow them then profile will remove from user's followings list
    and user will remove from profile followers list
    :param request
    :param following:slug of following profile
    :return: redirect to profile-detail-view url of following profile
    """
    profile = Profile.objects.get(email=request.user)
    if request.method == "POST":
        following = Profile.objects.get(slug=following)
        profile.following.remove(following)
        following.follower.remove(profile)

        return redirect('profiles:profile-detail-view', following.slug)

@login_required()
def remove_follower(request, follower):
    """
    if someone follows user,user can remove him/she then profile will remove from user's followers list
    and user will remove from profile followings list
    :param request
    :param follower:slug of follower profile
    :return: redirect to profile-detail-view url of following profile
    """
    profile = Profile.objects.get(email=request.user)
    if request.method == "POST":
        follower = Profile.objects.get(slug=follower)
        profile.follower.remove(follower)
        follower.following.remove(profile)

        return redirect('profiles:profile-detail-view', follower.slug)

@login_required()
def autocomplete_search(request):
    """
    in search page user can search in profiles and before Posting request suggested users that
    search phrase contains in their email will show,then by posting request if profile exists it redirect to
    profile page ,else show the message:profile dose not exist.
    :param request:
    :return: render of request,search.html and context or redirect to profile.get_absolute_url
    """
    if request.method == "GET":
        if 'term' in request.GET:
            qs = Profile.objects.filter(email__icontains=request.GET.get('term'))
            emails = list()
            for profile in qs:
                emails.append(profile.email)
            return JsonResponse(emails, safe=False)
        return render(request, 'profiles/search.html')
    if request.method == "POST":
        email = request.POST.get('profile')
        if Profile.objects.filter(email=email).exists():
            profile = Profile.objects.get(email=email)
            return redirect(profile.get_absolute_url())
        else:
            is_exist = False
            return render(request, 'profiles/search.html', {'is_exist': is_exist, 'msg': "profile dose not exist"})


