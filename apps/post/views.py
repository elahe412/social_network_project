from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from apps.post.forms import PostModelForm, CommentModelform
from apps.post.models import Post, Like, Comment
from apps.profiles.models import Profile


@login_required
def create_new_post(request):
    p_form = PostModelForm()
    post_added = False
    profile = Profile.objects.get(email=request.user)

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
            return redirect("posts:main-post-view")
    context = {
        'p_form': p_form,
        'post_added': post_added}
    return render(request, 'post/new_post.html', context)


@login_required
def post_list_view(request):
    qs = Post.objects.all()
    c_form = CommentModelform()
    profile = Profile.objects.get(email=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 5)

    if 'submit_c_form' in request.POST:
        c_form = CommentModelform(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelform()
            return redirect("posts:main-post-view")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        # 'qs': qs,
        'profile': profile,
        'c_form': c_form,
    }
    return render(request, 'post/main.html', context)


def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(email=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post_obj.save()
        like.save()

    return redirect('posts:main-post-view')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post')

        return obj


class PostUpdateView(UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'post/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(email=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the author of the post')
            return super().form_invalid(form)


class CommentDelete(DeleteView):
    template_name = 'post/confirm_del.html'
    model = Comment
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.user.email == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post')

        return obj


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    c_form = CommentModelform()

    profile = Profile.objects.get(email=request.user)

    if 'submit_c_form' in request.POST:
        c_form = CommentModelform(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelform()
            return redirect('posts:post-detail-view', pk=pk)

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(email=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post_obj.save()
        like.save()

    context = {
        'post': post,
        'profile': profile,
        'c_form': c_form,
    }
    return render(request, 'post/post_detail.html', context)
