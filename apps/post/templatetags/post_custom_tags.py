from django import template
from django.utils import timezone
import random

from apps.profiles.models import FollowRequest, Profile

register = template.Library()


@register.filter(name='age')
def post_age(publish_date):
    """
    :param publish_date: this will be created date of post and comment
    :return: a string that depends on how long has it been since publish date
    """
    age = timezone.now() - publish_date
    days, seconds = age.days, age.seconds
    hours = days * 24 + seconds // 3600
    month = days // 30
    if hours <= 1:
        return ' few moments ago'
    if hours <= 24:
        return '{} hours ago'.format(hours)
    if hours > 24:
        return '{} days ago'.format(days)
    if days <= 30:
        return '{} days ago'.format(days)
    if days <= 365:
        return '{} months ago'.format(month)


@register.filter(name='counting')
def number_of_requests(user):
    return FollowRequest.objects.filter(following=user).count()


@register.inclusion_tag('sidebar.html')
def random_profiles(user):
    user_followings = user.get_followings()
    all_profiles = Profile.objects.all()
    profiles = [x for x in all_profiles if (x not in user_followings and x.email != user)]
    random_profiles = random.choices(profiles, k=3)
    return {'random_profiles': random_profiles}
