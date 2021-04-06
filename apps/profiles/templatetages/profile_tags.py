import random
from django import template
from apps.profiles.models import Profile

register = template.Library()


@register.inclusion_tag('sidebar.html')
def random_profiles(user):
    user_followings = user.get_followings()
    all_profiles = Profile.objects.all()
    profiles = [x for x in all_profiles if (x not in user_followings and x.email != user)]
    random_profiles = set(random.choices(profiles, k=2))
    return {'random_profiles': random_profiles}
