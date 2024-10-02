# myapp/templatetags/custom_filters.py
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def first_name(full_name):
    return full_name.split()[0] if full_name else ''

    