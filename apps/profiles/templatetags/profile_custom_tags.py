from django import template

from apps.profiles.models import FollowRequest

register = template.Library()


@register.filter(name='counting')
def number_of_requests(user):
    return FollowRequest.objects.filter(following=user).count()
