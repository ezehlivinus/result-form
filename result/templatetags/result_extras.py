import math
from django import template

register = template.Library()


@register.simple_tag
def add(*args):
    return sum(args)

