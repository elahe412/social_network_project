from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from apps.profiles.managers import CustomUserManager


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_profiles_to_follow(self, following):
        profiles_list = [profile for profile in Profile.objects.all().exclude(user=following)]
        return profiles_list


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default='', blank=True, max_length=300)
    avatar = models.ImageField(upload_to='avatars/', default='avatar.png')
    website = models.URLField(max_length=300, blank=True)
    GENDER = [('Female', 'Female'), ('Male', 'Male')]
    gender = models.CharField(choices=GENDER, max_length=6, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    follower = models.ManyToManyField('profiles.Profile', blank=True, related_name='profile')
    following = models.ManyToManyField('profiles.Profile', blank=True, related_name='followings')
    slug = AutoSlugField(populate_from=['email'], unique=True)
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    profiles = ProfileManager()

    def __str__(self):
        return '{}'.format(self.email)

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_followers(self):
        return self.follower.all()

    def get_followings(self):
        return self.following.all()

    def get_followings_no(self):
        return self.following.all().count()

    def get_followers_no(self):
        return self.follower.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    # they should be deleted:

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked


class FollowRequestManager(models.Manager):
    def requests_received(self, following):
        qs = FollowRequest.objects.filter(following=following, status='send')
        return qs


class FollowRequest(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_follows")
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_is_followed")
    STATUS_CHOICES = (('send', 'send'), ('accepted', 'accepted'))
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = FollowRequestManager()