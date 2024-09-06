# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def first_name(full_name):
    return full_name.split()[0] if full_name else ''
