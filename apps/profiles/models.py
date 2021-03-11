from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models
from django_extensions.db.fields import AutoSlugField


# class ProfileManager(models.Manager):
#     def get_all_profiles_to_invite(self, following):
#         profiles = Profile.objects.all().exclude(user=following)
#         profile = Profile.objects.get(user=following)
#         qs = Follow.objects.filter(Q(following=profile) | Q(follower=profile))
#
#         accepted = set([])
#         for rel in qs:
#             if rel.status == 'accepted':
#                 accepted.add(rel.receiver)
#                 accepted.add(rel.sender)
#         print(accepted)
#
#         available = [profile for profile in profiles if profile not in accepted]
#         print(available)
#         return available
#
#     def get_all_profiles(self, me):
#         profiles = Profile.objects.all().exclude(user=me)
#         return profiles
# from apps.profiles.managers import UserManager


class Profile(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True, max_length=300)
    website = models.URLField(max_length=300, blank=True)
    GENDER = [('Female', 'Female'), ('Male', 'Male')]
    gender = models.CharField(choices=GENDER, max_length=6, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # followers = models.ManyToManyField(User, blank=True, related_name='followers')
    # following = models.ManyToManyField(User, blank=True, related_name='following')
    slug = AutoSlugField(populate_from=['email'], unique=True, )
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = UserManager()

    def __str__(self):
        return '{}'.format(self.email)

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

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


#
# class FollowManager(models.Manager):
#     def invitations_received(self, follower):
#         qs = Follow.objects.filter(follower=follower, status='send')
#         return qs


class Follow(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_follows")
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="who_is_followed")
    STATUS_CHOICES = (('send', 'send'), ('accepted', 'accepted'), ('reject', 'reject'))
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    # objects=FollowManager()
