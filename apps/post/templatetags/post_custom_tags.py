from django import template
from django.utils import timezone

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
    if days <= 1:
        return '{} hours ago'.format(hours)
    if days <= 30:
        return '{} days ago'.format(days)
    if days <= 365:
        return '{} months ago'.format(month)
