from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from apps.profiles.managers import CustomUserManager


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)

    # this fields are optional in editing profile
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default='', blank=True, max_length=300)
    avatar = models.ImageField(upload_to='avatars/', default='avatar.png')
    website = models.URLField(max_length=300, blank=True)
    GENDER = [('Female', 'Female'), ('Male', 'Male')]
    gender = models.CharField(choices=GENDER, max_length=6, blank=True)

    # time of create and update the profile
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # list of followers and followings of profile
    follower = models.ManyToManyField('profiles.Profile', blank=True, related_name='profile')
    following = models.ManyToManyField('profiles.Profile', blank=True, related_name='followings')

    slug = AutoSlugField(populate_from=['email'], unique=True)
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)

    # profile register and login with email,this will be the username of the profile object
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{}'.format(self.email)

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_followers(self):
        """
        :return: list of profile's followers
        """
        return self.follower.all()

    def get_followings(self):
        """
        :return: list of profile's followings
        """
        return self.following.all()

    def get_followings_no(self):
        """
        :return: number of profile's followings
        """
        return self.following.all().count()

    def get_followers_no(self):
        """
        :return: number of profile's followers
        """
        return self.follower.all().count()

    def get_posts_no(self):
        """
        :return: number of profile's posts
        """
        return self.posts.all().count()

    def get_all_authors_posts(self):
        """
        :return: list of profile's posts
        """
        return self.posts.all()


class FollowRequestManager(models.Manager):
    def requests_received(self, following):
        """
        this function get following profile and return list of follow requests that sent to hem/her
        :param following
        :return: qs
        """
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
